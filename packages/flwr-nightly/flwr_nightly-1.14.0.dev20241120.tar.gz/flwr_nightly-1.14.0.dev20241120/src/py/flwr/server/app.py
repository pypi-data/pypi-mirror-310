# Copyright 2020 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower server app."""

import argparse
import csv
import importlib.util
import subprocess
import sys
import threading
from collections.abc import Sequence
from logging import DEBUG, INFO, WARN
from pathlib import Path
from time import sleep
from typing import Optional

import grpc
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    load_ssh_private_key,
    load_ssh_public_key,
)

from flwr.common import GRPC_MAX_MESSAGE_LENGTH, EventType, event
from flwr.common.address import parse_address
from flwr.common.args import try_obtain_server_certificates
from flwr.common.config import get_flwr_dir, parse_config_args
from flwr.common.constant import (
    CLIENT_OCTET,
    EXEC_API_DEFAULT_SERVER_ADDRESS,
    FLEET_API_GRPC_BIDI_DEFAULT_ADDRESS,
    FLEET_API_GRPC_RERE_DEFAULT_ADDRESS,
    FLEET_API_REST_DEFAULT_ADDRESS,
    ISOLATION_MODE_PROCESS,
    ISOLATION_MODE_SUBPROCESS,
    MISSING_EXTRA_REST,
    SERVER_OCTET,
    SERVERAPPIO_API_DEFAULT_SERVER_ADDRESS,
    SIMULATIONIO_API_DEFAULT_SERVER_ADDRESS,
    TRANSPORT_TYPE_GRPC_ADAPTER,
    TRANSPORT_TYPE_GRPC_RERE,
    TRANSPORT_TYPE_REST,
)
from flwr.common.exit_handlers import register_exit_handlers
from flwr.common.logger import log, warn_deprecated_feature
from flwr.common.secure_aggregation.crypto.symmetric_encryption import (
    private_key_to_bytes,
    public_key_to_bytes,
)
from flwr.proto.fleet_pb2_grpc import (  # pylint: disable=E0611
    add_FleetServicer_to_server,
)
from flwr.proto.grpcadapter_pb2_grpc import add_GrpcAdapterServicer_to_server
from flwr.superexec.app import load_executor
from flwr.superexec.exec_grpc import run_exec_api_grpc
from flwr.superexec.simulation import SimulationEngine

from .client_manager import ClientManager
from .history import History
from .server import Server, init_defaults, run_fl
from .server_config import ServerConfig
from .strategy import Strategy
from .superlink.driver.serverappio_grpc import run_serverappio_api_grpc
from .superlink.ffs.ffs_factory import FfsFactory
from .superlink.fleet.grpc_adapter.grpc_adapter_servicer import GrpcAdapterServicer
from .superlink.fleet.grpc_bidi.grpc_server import (
    generic_create_grpc_server,
    start_grpc_server,
)
from .superlink.fleet.grpc_rere.fleet_servicer import FleetServicer
from .superlink.fleet.grpc_rere.server_interceptor import AuthenticateServerInterceptor
from .superlink.linkstate import LinkStateFactory
from .superlink.simulation.simulationio_grpc import run_simulationio_api_grpc

DATABASE = ":flwr-in-memory-state:"
BASE_DIR = get_flwr_dir() / "superlink" / "ffs"


def start_server(  # pylint: disable=too-many-arguments,too-many-locals
    *,
    server_address: str = FLEET_API_GRPC_BIDI_DEFAULT_ADDRESS,
    server: Optional[Server] = None,
    config: Optional[ServerConfig] = None,
    strategy: Optional[Strategy] = None,
    client_manager: Optional[ClientManager] = None,
    grpc_max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
    certificates: Optional[tuple[bytes, bytes, bytes]] = None,
) -> History:
    """Start a Flower server using the gRPC transport layer.

    Warning
    -------
    This function is deprecated since 1.13.0. Use the :code:`flower-superlink` command
    instead to start a SuperLink.

    Parameters
    ----------
    server_address : Optional[str]
        The IPv4 or IPv6 address of the server. Defaults to `"[::]:8080"`.
    server : Optional[flwr.server.Server] (default: None)
        A server implementation, either `flwr.server.Server` or a subclass
        thereof. If no instance is provided, then `start_server` will create
        one.
    config : Optional[ServerConfig] (default: None)
        Currently supported values are `num_rounds` (int, default: 1) and
        `round_timeout` in seconds (float, default: None).
    strategy : Optional[flwr.server.Strategy] (default: None).
        An implementation of the abstract base class
        `flwr.server.strategy.Strategy`. If no strategy is provided, then
        `start_server` will use `flwr.server.strategy.FedAvg`.
    client_manager : Optional[flwr.server.ClientManager] (default: None)
        An implementation of the abstract base class
        `flwr.server.ClientManager`. If no implementation is provided, then
        `start_server` will use
        `flwr.server.client_manager.SimpleClientManager`.
    grpc_max_message_length : int (default: 536_870_912, this equals 512MB)
        The maximum length of gRPC messages that can be exchanged with the
        Flower clients. The default should be sufficient for most models.
        Users who train very large models might need to increase this
        value. Note that the Flower clients need to be started with the
        same value (see `flwr.client.start_client`), otherwise clients will
        not know about the increased limit and block larger messages.
    certificates : Tuple[bytes, bytes, bytes] (default: None)
        Tuple containing root certificate, server certificate, and private key
        to start a secure SSL-enabled server. The tuple is expected to have
        three bytes elements in the following order:

            * CA certificate.
            * server certificate.
            * server private key.

    Returns
    -------
    hist : flwr.server.history.History
        Object containing training and evaluation metrics.

    Examples
    --------
    Starting an insecure server:

    >>> start_server()

    Starting an SSL-enabled server:

    >>> start_server(
    >>>     certificates=(
    >>>         Path("/crts/root.pem").read_bytes(),
    >>>         Path("/crts/localhost.crt").read_bytes(),
    >>>         Path("/crts/localhost.key").read_bytes()
    >>>     )
    >>> )
    """
    msg = (
        "flwr.server.start_server() is deprecated."
        "\n\tInstead, use the `flower-superlink` CLI command to start a SuperLink "
        "as shown below:"
        "\n\n\t\t$ flower-superlink --insecure"
        "\n\n\tTo view usage and all available options, run:"
        "\n\n\t\t$ flower-superlink --help"
        "\n\n\tUsing `start_server()` is deprecated."
    )
    warn_deprecated_feature(name=msg)

    event(EventType.START_SERVER_ENTER)

    # Parse IP address
    parsed_address = parse_address(server_address)
    if not parsed_address:
        sys.exit(f"Server IP address ({server_address}) cannot be parsed.")
    host, port, is_v6 = parsed_address
    address = f"[{host}]:{port}" if is_v6 else f"{host}:{port}"

    # Initialize server and server config
    initialized_server, initialized_config = init_defaults(
        server=server,
        config=config,
        strategy=strategy,
        client_manager=client_manager,
    )
    log(
        INFO,
        "Starting Flower server, config: %s",
        initialized_config,
    )

    # Start gRPC server
    grpc_server = start_grpc_server(
        client_manager=initialized_server.client_manager(),
        server_address=address,
        max_message_length=grpc_max_message_length,
        certificates=certificates,
    )
    log(
        INFO,
        "Flower ECE: gRPC server running (%s rounds), SSL is %s",
        initialized_config.num_rounds,
        "enabled" if certificates is not None else "disabled",
    )

    # Start training
    hist = run_fl(
        server=initialized_server,
        config=initialized_config,
    )

    # Stop the gRPC server
    grpc_server.stop(grace=1)

    event(EventType.START_SERVER_LEAVE)

    return hist


# pylint: disable=too-many-branches, too-many-locals, too-many-statements
def run_superlink() -> None:
    """Run Flower SuperLink (ServerAppIo API and Fleet API)."""
    args = _parse_args_run_superlink().parse_args()

    log(INFO, "Starting Flower SuperLink")

    event(EventType.RUN_SUPERLINK_ENTER)

    # Warn unused options
    if args.flwr_dir is not None:
        log(
            WARN, "The `--flwr-dir` option is currently not in use and will be ignored."
        )

    # Parse IP addresses
    serverappio_address, _, _ = _format_address(args.serverappio_api_address)
    exec_address, _, _ = _format_address(args.exec_api_address)
    simulationio_address, _, _ = _format_address(args.simulationio_api_address)

    # Obtain certificates
    certificates = try_obtain_server_certificates(args, args.fleet_api_type)

    # Initialize StateFactory
    state_factory = LinkStateFactory(args.database)

    # Initialize FfsFactory
    ffs_factory = FfsFactory(args.storage_dir)

    # Start Exec API
    executor = load_executor(args)
    exec_server: grpc.Server = run_exec_api_grpc(
        address=exec_address,
        state_factory=state_factory,
        ffs_factory=ffs_factory,
        executor=executor,
        certificates=certificates,
        config=parse_config_args(
            [args.executor_config] if args.executor_config else args.executor_config
        ),
    )
    grpc_servers = [exec_server]

    # Determine Exec plugin
    # If simulation is used, don't start ServerAppIo and Fleet APIs
    sim_exec = isinstance(executor, SimulationEngine)

    bckg_threads = []

    if sim_exec:
        simulationio_server: grpc.Server = run_simulationio_api_grpc(
            address=simulationio_address,
            state_factory=state_factory,
            ffs_factory=ffs_factory,
            certificates=certificates,
        )
        grpc_servers.append(simulationio_server)

    else:
        # Start ServerAppIo API
        serverappio_server: grpc.Server = run_serverappio_api_grpc(
            address=serverappio_address,
            state_factory=state_factory,
            ffs_factory=ffs_factory,
            certificates=None,  # ServerAppIo API doesn't support SSL yet
        )
        grpc_servers.append(serverappio_server)

        # Start Fleet API
        if not args.fleet_api_address:
            if args.fleet_api_type in [
                TRANSPORT_TYPE_GRPC_RERE,
                TRANSPORT_TYPE_GRPC_ADAPTER,
            ]:
                args.fleet_api_address = FLEET_API_GRPC_RERE_DEFAULT_ADDRESS
            elif args.fleet_api_type == TRANSPORT_TYPE_REST:
                args.fleet_api_address = FLEET_API_REST_DEFAULT_ADDRESS

        fleet_address, host, port = _format_address(args.fleet_api_address)

        num_workers = args.fleet_api_num_workers
        if num_workers != 1:
            log(
                WARN,
                "The Fleet API currently supports only 1 worker. "
                "You have specified %d workers. "
                "Support for multiple workers will be added in future releases. "
                "Proceeding with a single worker.",
                args.fleet_api_num_workers,
            )
            num_workers = 1

        if args.fleet_api_type == TRANSPORT_TYPE_REST:
            if (
                importlib.util.find_spec("requests")
                and importlib.util.find_spec("starlette")
                and importlib.util.find_spec("uvicorn")
            ) is None:
                sys.exit(MISSING_EXTRA_REST)

            _, ssl_certfile, ssl_keyfile = (
                certificates if certificates is not None else (None, None, None)
            )

            fleet_thread = threading.Thread(
                target=_run_fleet_api_rest,
                args=(
                    host,
                    port,
                    ssl_keyfile,
                    ssl_certfile,
                    state_factory,
                    ffs_factory,
                    num_workers,
                ),
            )
            fleet_thread.start()
            bckg_threads.append(fleet_thread)
        elif args.fleet_api_type == TRANSPORT_TYPE_GRPC_RERE:
            maybe_keys = _try_setup_node_authentication(args, certificates)
            interceptors: Optional[Sequence[grpc.ServerInterceptor]] = None
            if maybe_keys is not None:
                (
                    node_public_keys,
                    server_private_key,
                    server_public_key,
                ) = maybe_keys
                state = state_factory.state()
                state.store_node_public_keys(node_public_keys)
                state.store_server_private_public_key(
                    private_key_to_bytes(server_private_key),
                    public_key_to_bytes(server_public_key),
                )
                log(
                    INFO,
                    "Node authentication enabled with %d known public keys",
                    len(node_public_keys),
                )
                interceptors = [AuthenticateServerInterceptor(state)]

            fleet_server = _run_fleet_api_grpc_rere(
                address=fleet_address,
                state_factory=state_factory,
                ffs_factory=ffs_factory,
                certificates=certificates,
                interceptors=interceptors,
            )
            grpc_servers.append(fleet_server)
        elif args.fleet_api_type == TRANSPORT_TYPE_GRPC_ADAPTER:
            fleet_server = _run_fleet_api_grpc_adapter(
                address=fleet_address,
                state_factory=state_factory,
                ffs_factory=ffs_factory,
                certificates=certificates,
            )
            grpc_servers.append(fleet_server)
        else:
            raise ValueError(f"Unknown fleet_api_type: {args.fleet_api_type}")

    if args.isolation == ISOLATION_MODE_SUBPROCESS:

        _octet, _colon, _port = serverappio_address.rpartition(":")
        io_address = (
            f"{CLIENT_OCTET}:{_port}" if _octet == SERVER_OCTET else serverappio_address
        )
        address = simulationio_address if sim_exec else io_address
        cmd = "flwr-simulation" if sim_exec else "flwr-serverapp"

        # Scheduler thread
        scheduler_th = threading.Thread(
            target=_flwr_scheduler,
            args=(
                state_factory,
                address,
                cmd,
            ),
        )
        scheduler_th.start()
        bckg_threads.append(scheduler_th)

    # Graceful shutdown
    register_exit_handlers(
        event_type=EventType.RUN_SUPERLINK_LEAVE,
        grpc_servers=grpc_servers,
        bckg_threads=bckg_threads,
    )

    # Block
    while True:
        if bckg_threads:
            for thread in bckg_threads:
                if not thread.is_alive():
                    sys.exit(1)
        exec_server.wait_for_termination(timeout=1)


def _flwr_scheduler(
    state_factory: LinkStateFactory,
    io_api_address: str,
    cmd: str,
) -> None:
    log(DEBUG, "Started %s scheduler thread.", cmd)

    state = state_factory.state()

    # Periodically check for a pending run in the LinkState
    while True:
        sleep(3)
        pending_run_id = state.get_pending_run_id()

        if pending_run_id:

            log(
                INFO,
                "Launching %s subprocess. Connects to SuperLink on %s",
                cmd,
                io_api_address,
            )
            # Start subprocess
            command = [
                cmd,
                "--run-once",
                "--serverappio-api-address",
                io_api_address,
                "--insecure",
            ]

            subprocess.Popen(  # pylint: disable=consider-using-with
                command,
                text=True,
            )


def _format_address(address: str) -> tuple[str, str, int]:
    parsed_address = parse_address(address)
    if not parsed_address:
        sys.exit(
            f"Address ({address}) cannot be parsed (expected: URL or IPv4 or IPv6)."
        )
    host, port, is_v6 = parsed_address
    return (f"[{host}]:{port}" if is_v6 else f"{host}:{port}", host, port)


def _try_setup_node_authentication(
    args: argparse.Namespace,
    certificates: Optional[tuple[bytes, bytes, bytes]],
) -> Optional[tuple[set[bytes], ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]]:
    if (
        not args.auth_list_public_keys
        and not args.auth_superlink_private_key
        and not args.auth_superlink_public_key
    ):
        return None

    if (
        not args.auth_list_public_keys
        or not args.auth_superlink_private_key
        or not args.auth_superlink_public_key
    ):
        sys.exit(
            "Authentication requires providing file paths for "
            "'--auth-list-public-keys', '--auth-superlink-private-key' and "
            "'--auth-superlink-public-key'. Provide all three to enable authentication."
        )

    if certificates is None:
        sys.exit(
            "Authentication requires secure connections. "
            "Please provide certificate paths to `--ssl-certfile`, "
            "`--ssl-keyfile`, and `—-ssl-ca-certfile` and try again."
        )

    node_keys_file_path = Path(args.auth_list_public_keys)
    if not node_keys_file_path.exists():
        sys.exit(
            "The provided path to the known public keys CSV file does not exist: "
            f"{node_keys_file_path}. "
            "Please provide the CSV file path containing known public keys "
            "to '--auth-list-public-keys'."
        )

    node_public_keys: set[bytes] = set()

    try:
        ssh_private_key = load_ssh_private_key(
            Path(args.auth_superlink_private_key).read_bytes(),
            None,
        )
        if not isinstance(ssh_private_key, ec.EllipticCurvePrivateKey):
            raise ValueError()
    except (ValueError, UnsupportedAlgorithm):
        sys.exit(
            "Error: Unable to parse the private key file in "
            "'--auth-superlink-private-key'. Authentication requires elliptic "
            "curve private and public key pair. Please ensure that the file "
            "path points to a valid private key file and try again."
        )

    try:
        ssh_public_key = load_ssh_public_key(
            Path(args.auth_superlink_public_key).read_bytes()
        )
        if not isinstance(ssh_public_key, ec.EllipticCurvePublicKey):
            raise ValueError()
    except (ValueError, UnsupportedAlgorithm):
        sys.exit(
            "Error: Unable to parse the public key file in "
            "'--auth-superlink-public-key'. Authentication requires elliptic "
            "curve private and public key pair. Please ensure that the file "
            "path points to a valid public key file and try again."
        )

    with open(node_keys_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for element in row:
                public_key = load_ssh_public_key(element.encode())
                if isinstance(public_key, ec.EllipticCurvePublicKey):
                    node_public_keys.add(public_key_to_bytes(public_key))
                else:
                    sys.exit(
                        "Error: Unable to parse the public keys in the CSV "
                        "file. Please ensure that the CSV file path points to a valid "
                        "known SSH public keys files and try again."
                    )
        return (
            node_public_keys,
            ssh_private_key,
            ssh_public_key,
        )


def _run_fleet_api_grpc_rere(
    address: str,
    state_factory: LinkStateFactory,
    ffs_factory: FfsFactory,
    certificates: Optional[tuple[bytes, bytes, bytes]],
    interceptors: Optional[Sequence[grpc.ServerInterceptor]] = None,
) -> grpc.Server:
    """Run Fleet API (gRPC, request-response)."""
    # Create Fleet API gRPC server
    fleet_servicer = FleetServicer(
        state_factory=state_factory,
        ffs_factory=ffs_factory,
    )
    fleet_add_servicer_to_server_fn = add_FleetServicer_to_server
    fleet_grpc_server = generic_create_grpc_server(
        servicer_and_add_fn=(fleet_servicer, fleet_add_servicer_to_server_fn),
        server_address=address,
        max_message_length=GRPC_MAX_MESSAGE_LENGTH,
        certificates=certificates,
        interceptors=interceptors,
    )

    log(INFO, "Flower ECE: Starting Fleet API (gRPC-rere) on %s", address)
    fleet_grpc_server.start()

    return fleet_grpc_server


def _run_fleet_api_grpc_adapter(
    address: str,
    state_factory: LinkStateFactory,
    ffs_factory: FfsFactory,
    certificates: Optional[tuple[bytes, bytes, bytes]],
) -> grpc.Server:
    """Run Fleet API (GrpcAdapter)."""
    # Create Fleet API gRPC server
    fleet_servicer = GrpcAdapterServicer(
        state_factory=state_factory,
        ffs_factory=ffs_factory,
    )
    fleet_add_servicer_to_server_fn = add_GrpcAdapterServicer_to_server
    fleet_grpc_server = generic_create_grpc_server(
        servicer_and_add_fn=(fleet_servicer, fleet_add_servicer_to_server_fn),
        server_address=address,
        max_message_length=GRPC_MAX_MESSAGE_LENGTH,
        certificates=certificates,
    )

    log(INFO, "Flower ECE: Starting Fleet API (GrpcAdapter) on %s", address)
    fleet_grpc_server.start()

    return fleet_grpc_server


# pylint: disable=import-outside-toplevel,too-many-arguments
# pylint: disable=too-many-positional-arguments
def _run_fleet_api_rest(
    host: str,
    port: int,
    ssl_keyfile: Optional[str],
    ssl_certfile: Optional[str],
    state_factory: LinkStateFactory,
    ffs_factory: FfsFactory,
    num_workers: int,
) -> None:
    """Run ServerAppIo API (REST-based)."""
    try:
        import uvicorn

        from flwr.server.superlink.fleet.rest_rere.rest_api import app as fast_api_app
    except ModuleNotFoundError:
        sys.exit(MISSING_EXTRA_REST)

    log(INFO, "Starting Flower REST server")

    # See: https://www.starlette.io/applications/#accessing-the-app-instance
    fast_api_app.state.STATE_FACTORY = state_factory
    fast_api_app.state.FFS_FACTORY = ffs_factory

    uvicorn.run(
        app="flwr.server.superlink.fleet.rest_rere.rest_api:app",
        port=port,
        host=host,
        reload=False,
        access_log=True,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
        workers=num_workers,
    )


def _parse_args_run_superlink() -> argparse.ArgumentParser:
    """Parse command line arguments for both ServerAppIo API and Fleet API."""
    parser = argparse.ArgumentParser(
        description="Start a Flower SuperLink",
    )

    _add_args_common(parser=parser)
    _add_args_serverappio_api(parser=parser)
    _add_args_fleet_api(parser=parser)
    _add_args_exec_api(parser=parser)
    _add_args_simulationio_api(parser=parser)

    return parser


def _add_args_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Run the server without HTTPS, regardless of whether certificate "
        "paths are provided. By default, the server runs with HTTPS enabled. "
        "Use this flag only if you understand the risks.",
    )
    parser.add_argument(
        "--flwr-dir",
        default=None,
        help="""The path containing installed Flower Apps.
        The default directory is:

        - `$FLWR_HOME/` if `$FLWR_HOME` is defined
        - `$XDG_DATA_HOME/.flwr/` if `$XDG_DATA_HOME` is defined
        - `$HOME/.flwr/` in all other cases
        """,
    )
    parser.add_argument(
        "--ssl-certfile",
        help="Fleet API server SSL certificate file (as a path str) "
        "to create a secure connection.",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--ssl-keyfile",
        help="Fleet API server SSL private key file (as a path str) "
        "to create a secure connection.",
        type=str,
    )
    parser.add_argument(
        "--ssl-ca-certfile",
        help="Fleet API server SSL CA certificate file (as a path str) "
        "to create a secure connection.",
        type=str,
    )
    parser.add_argument(
        "--isolation",
        default=ISOLATION_MODE_SUBPROCESS,
        required=False,
        choices=[
            ISOLATION_MODE_SUBPROCESS,
            ISOLATION_MODE_PROCESS,
        ],
        help="Isolation mode when running a `ServerApp` (`subprocess` by default, "
        "possible values: `subprocess`, `process`). Use `subprocess` to configure "
        "SuperLink to run a `ServerApp` in a subprocess. Use `process` to indicate "
        "that a separate independent process gets created outside of SuperLink.",
    )
    parser.add_argument(
        "--database",
        help="A string representing the path to the database "
        "file that will be opened. Note that passing ':memory:' "
        "will open a connection to a database that is in RAM, "
        "instead of on disk. If nothing is provided, "
        "Flower will just create a state in memory.",
        default=DATABASE,
    )
    parser.add_argument(
        "--storage-dir",
        help="The base directory to store the objects for the Flower File System.",
        default=BASE_DIR,
    )
    parser.add_argument(
        "--auth-list-public-keys",
        type=str,
        help="A CSV file (as a path str) containing a list of known public "
        "keys to enable authentication.",
    )
    parser.add_argument(
        "--auth-superlink-private-key",
        type=str,
        help="The SuperLink's private key (as a path str) to enable authentication.",
    )
    parser.add_argument(
        "--auth-superlink-public-key",
        type=str,
        help="The SuperLink's public key (as a path str) to enable authentication.",
    )


def _add_args_serverappio_api(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--serverappio-api-address",
        default=SERVERAPPIO_API_DEFAULT_SERVER_ADDRESS,
        help="ServerAppIo API (gRPC) server address (IPv4, IPv6, or a domain name). "
        f"By default, it is set to {SERVERAPPIO_API_DEFAULT_SERVER_ADDRESS}.",
    )


def _add_args_fleet_api(parser: argparse.ArgumentParser) -> None:
    # Fleet API transport layer type
    parser.add_argument(
        "--fleet-api-type",
        default=TRANSPORT_TYPE_GRPC_RERE,
        type=str,
        choices=[
            TRANSPORT_TYPE_GRPC_RERE,
            TRANSPORT_TYPE_GRPC_ADAPTER,
            TRANSPORT_TYPE_REST,
        ],
        help="Start a gRPC-rere or REST (experimental) Fleet API server.",
    )
    parser.add_argument(
        "--fleet-api-address",
        help="Fleet API server address (IPv4, IPv6, or a domain name).",
    )
    parser.add_argument(
        "--fleet-api-num-workers",
        default=1,
        type=int,
        help="Set the number of concurrent workers for the Fleet API server.",
    )


def _add_args_exec_api(parser: argparse.ArgumentParser) -> None:
    """Add command line arguments for Exec API."""
    parser.add_argument(
        "--exec-api-address",
        help="Exec API server address (IPv4, IPv6, or a domain name) "
        f"By default, it is set to {EXEC_API_DEFAULT_SERVER_ADDRESS}.",
        default=EXEC_API_DEFAULT_SERVER_ADDRESS,
    )
    parser.add_argument(
        "--executor",
        help="For example: `deployment:exec` or `project.package.module:wrapper.exec`. "
        "The default is `flwr.superexec.deployment:executor`",
        default="flwr.superexec.deployment:executor",
    )
    parser.add_argument(
        "--executor-dir",
        help="The directory for the executor.",
        default=".",
    )
    parser.add_argument(
        "--executor-config",
        help="Key-value pairs for the executor config, separated by spaces. "
        "For example:\n\n`--executor-config 'verbose=true "
        'root-certificates="certificates/superlink-ca.crt"\'`',
    )


def _add_args_simulationio_api(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--simulationio-api-address",
        default=SIMULATIONIO_API_DEFAULT_SERVER_ADDRESS,
        help="SimulationIo API (gRPC) server address (IPv4, IPv6, or a domain name)."
        f"By default, it is set to {SIMULATIONIO_API_DEFAULT_SERVER_ADDRESS}.",
    )
