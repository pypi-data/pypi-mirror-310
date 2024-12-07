"""Setup the service."""

from __future__ import annotations

import asyncio
import contextlib
import functools
import shutil
import subprocess
import uuid
from typing import TYPE_CHECKING, cast

import docker
import docker.errors
from composition_menus import composition_menu
from compositions import IMAGES
from docker.models.containers import Container
from docker.models.images import Image
from kivy.clock import mainthread
from reducer import image_reducer, reducer_id
from redux import CombineReducerRegisterAction
from ubo_gui.constants import DANGER_COLOR, SUCCESS_COLOR, WARNING_COLOR
from ubo_gui.menu.types import ActionItem, HeadedMenu, HeadlessMenu, Item, SubMenuItem

from ubo_app.constants import CONFIG_PATH, DOCKER_CREDENTIALS_TEMPLATE
from ubo_app.logging import logger
from ubo_app.store.core.types import (
    DeregisterRegularAppAction,
    RegisterRegularAppAction,
    RegisterSettingAppAction,
    SettingsCategory,
)
from ubo_app.store.input.types import InputFieldDescription, InputFieldType
from ubo_app.store.main import store
from ubo_app.store.services.docker import (
    DockerImageRegisterAppEvent,
    DockerLoadImagesEvent,
    DockerRemoveUsernameAction,
    DockerSetStatusAction,
    DockerStatus,
    DockerStoreUsernameAction,
)
from ubo_app.store.services.notifications import (
    Chime,
    Importance,
    Notification,
    NotificationDisplayType,
    NotificationExtraInformation,
    NotificationsAddAction,
)
from ubo_app.utils import secrets
from ubo_app.utils.apt import is_package_installed
from ubo_app.utils.async_ import create_task
from ubo_app.utils.input import ubo_input
from ubo_app.utils.log_process import log_async_process
from ubo_app.utils.monitor_unit import monitor_unit
from ubo_app.utils.persistent_store import register_persistent_store
from ubo_app.utils.server import send_command

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from pathlib import Path

COMPOSITIONS_PATH = CONFIG_PATH / 'docker_compositions'


def install_docker() -> None:
    """Install Docker."""

    async def act() -> None:
        store.dispatch(DockerSetStatusAction(status=DockerStatus.INSTALLING))
        result = await send_command(
            'docker',
            'install',
            has_output=True,
        )
        if result != 'installed':
            store.dispatch(
                NotificationsAddAction(
                    notification=Notification(
                        title='Docker',
                        content='Failed to install',
                        display_type=NotificationDisplayType.STICKY,
                        color=DANGER_COLOR,
                        icon='󰜺',
                        chime=Chime.FAILURE,
                    ),
                ),
            )
        await check_docker()

    create_task(act())


def run_docker() -> None:
    """Install Docker."""

    async def act() -> None:
        await send_command('docker', 'start')
        store.dispatch(DockerSetStatusAction(status=DockerStatus.UNKNOWN))

    create_task(act())


def stop_docker() -> None:
    """Install Docker."""

    async def act() -> None:
        await send_command('docker', 'stop')
        store.dispatch(DockerSetStatusAction(status=DockerStatus.UNKNOWN))

    create_task(act())


async def check_docker() -> None:
    """Check if Docker is installed."""
    from container_ import update_container

    is_installed = await is_package_installed('docker')

    is_running = False
    with contextlib.suppress(Exception):
        docker_client = docker.from_env()
        is_running = docker_client.ping()

        for container in docker_client.containers.list(all=True):
            if not isinstance(container, Container):
                continue

            with contextlib.suppress(docker.errors.DockerException):
                container_image = container.image
                for image_id, image_description in IMAGES.items():
                    if (
                        isinstance(container_image, Image)
                        and image_description.path in container_image.tags
                    ):
                        update_container(image_id, container)

        docker_client.close()

    if is_running:
        store.dispatch(DockerSetStatusAction(status=DockerStatus.RUNNING))
    elif is_installed:
        store.dispatch(DockerSetStatusAction(status=DockerStatus.NOT_RUNNING))
    else:
        store.dispatch(DockerSetStatusAction(status=DockerStatus.NOT_INSTALLED))


@store.autorun(lambda state: state.docker.service.status)
def setup_menu(status: DockerStatus) -> HeadedMenu:
    """Get the menu items for the Docker service."""
    title = 'Setup Docker'
    return {
        DockerStatus.UNKNOWN: HeadedMenu(
            title=title,
            heading='Checking',
            sub_heading='Checking Docker service status',
            items=[],
            placeholder='',
        ),
        DockerStatus.NOT_INSTALLED: HeadedMenu(
            title=title,
            heading='Docker is not Installed',
            sub_heading='Install it to enjoy the power of Docker on your Ubo pod',
            items=[
                ActionItem(
                    label='Install Docker',
                    icon='󰶮',
                    action=install_docker,
                ),
            ],
        ),
        DockerStatus.INSTALLING: HeadedMenu(
            title=title,
            heading='Installing...',
            sub_heading='Docker is being installed',
            items=[],
            placeholder='',
        ),
        DockerStatus.NOT_RUNNING: HeadedMenu(
            title=title,
            heading='Docker is not Running',
            sub_heading='Run it to enjoy the power of Docker on your Ubo pod',
            items=[
                ActionItem(
                    label='Start Docker',
                    icon='󰐊',
                    action=run_docker,
                ),
            ],
        ),
        DockerStatus.RUNNING: HeadedMenu(
            title=title,
            heading='Docker is Running',
            sub_heading='Enjoy the power of Docker on your Ubo pod',
            items=[
                ActionItem(
                    label='Stop Docker',
                    icon='󰓛',
                    action=stop_docker,
                ),
            ],
        ),
        DockerStatus.ERROR: HeadedMenu(
            title=title,
            heading='Docker Error',
            sub_heading='Please check the logs for more information',
            items=[],
            placeholder='',
        ),
    }[status]


def setup_menu_action() -> Callable[[], HeadedMenu]:
    """Get the menu items for the Docker service."""
    create_task(check_docker())
    return setup_menu


def input_credentials() -> None:
    """Input the Docker credentials."""

    async def act() -> None:
        try:
            credentials = (
                await ubo_input(
                    prompt='Enter Docker Credentials',
                    qr_code_generation_instructions=NotificationExtraInformation(
                        text="""To generate your QR code for login, format your \
details by separating your service, username, and password with the pipe symbol. For \
example, format it as "docker.io|johndoe|password" and then convert this text into a \
QR code. If you omit the service name, "docker.io" will automatically be used as the \
default.""",
                        piper_text="""To generate your QR code for login, format your \
details by separating your service, username, and password with the pipe symbol. For \
example, format it as docker.ay o pipe johndoe pipe password and then convert this \
text into a QR code. If you omit the service name, docker.ay o will automatically be \
used as the default.""",
                        picovoice_text="""To generate your {QR|K Y UW AA R} code for \
login, format your details by separating your service, username, and password with the \
pipe symbol. For example, format it as "docker {.|D AA T} io {.|P AY P} johndoe \
{.|P AY P} password" and then convert this text into a {QR|K Y UW AA R} code. If you \
omit the service name, "docker {.|D AA T} io" will automatically be used as the \
default.""",
                    ),
                    pattern=r'^(?P<Service>[^|]*)\|(?P<Username>[^|]*)\|(?P<Password>[^|]*)$|'
                    r'(?P<Username_>^[^|]*)|(?P<Password_>[^|]*)$',
                    fields=[
                        InputFieldDescription(
                            name='Service',
                            label='Service',
                            type=InputFieldType.TEXT,
                            description='The service name',
                            default='docker.io',
                            required=False,
                        ),
                        InputFieldDescription(
                            name='Username',
                            label='Username',
                            type=InputFieldType.TEXT,
                            required=True,
                        ),
                        InputFieldDescription(
                            name='Password',
                            label='Password',
                            type=InputFieldType.PASSWORD,
                            required=True,
                        ),
                    ],
                )
            )[1]
            if not credentials:
                return
            username = credentials.get('Username', credentials.get('Username_', ''))
            password = credentials.get('Password', credentials.get('Password_', ''))
            registry = credentials.get('Service', 'docker.io')
            username = cast(str, username).strip()
            password = cast(str, password).strip()
            registry = cast(str, registry).strip()
            docker_client = docker.from_env()
            docker_client.login(
                username=username,
                password=password,
                registry=registry,
            )
            secrets.write_secret(
                key=DOCKER_CREDENTIALS_TEMPLATE.format(registry),
                value=password,
            )
            store.dispatch(
                DockerStoreUsernameAction(registry=registry, username=username),
            )
        except asyncio.CancelledError:
            pass
        except docker.errors.APIError as exception:
            explanation = exception.explanation or (
                exception.response.content.decode('utf8') if exception.response else ''
            )
            store.dispatch(
                NotificationsAddAction(
                    notification=Notification(
                        title='Docker Credentials Error',
                        content='Invalid credentials',
                        extra_information=NotificationExtraInformation(
                            text=explanation,
                        ),
                        importance=Importance.HIGH,
                    ),
                ),
            )

    create_task(act())


class _CompositionItems:
    def __init__(
        self: _CompositionItems,
        item: Path,
        on_delete: Callable[[], None],
    ) -> None:
        self.callback = None
        self.is_running = False
        self.is_pending = False
        self.item = item
        self.on_delete = on_delete
        create_task(self.check())

    @mainthread
    def update(self: _CompositionItems) -> None:
        if self.callback:
            self.callback(self())

    async def stop_composition(self: _CompositionItems) -> None:
        """Stop the composition."""
        self.is_pending = True
        self.update()
        stop_process = await asyncio.subprocess.create_subprocess_exec(
            'docker',
            'compose',
            'down',
            cwd=self.item,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        await stop_process.wait()
        await log_async_process(stop_process)
        self.is_pending = False
        self.update()
        await asyncio.sleep(1)
        self.update()

    async def run_composition(self: _CompositionItems) -> None:
        """Run the composition."""
        self.is_pending = True
        self.update()
        run_process = await asyncio.subprocess.create_subprocess_exec(
            'docker',
            'compose',
            'up',
            '-d',
            cwd=self.item,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        await run_process.wait()
        await log_async_process(run_process)
        self.is_pending = False
        self.update()
        await asyncio.sleep(1)
        self.update()

    async def check(self: _CompositionItems) -> None:
        check_process = await asyncio.subprocess.create_subprocess_exec(
            'docker',
            'compose',
            'ps',
            '--quiet',
            cwd=self.item,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        await check_process.wait()
        await log_async_process(check_process)
        self.is_running = (
            check_process.stdout is not None
            and (await check_process.stdout.read()) != b''
        )
        self.update()

    def delete(self: _CompositionItems) -> None:
        """Delete the composition."""
        shutil.rmtree(self.item)
        self.on_delete()

    def __call__(self: _CompositionItems) -> list[Item]:
        items: list[Item] = []

        if self.is_pending:
            items.append(
                Item(
                    key='start-stop',
                    icon='',
                    background_color='black',
                    color='white',
                ),
            )
        elif self.is_running:
            items.append(
                ActionItem(
                    key='start-stop',
                    label='Stop',
                    icon='󰓛',
                    background_color=WARNING_COLOR,
                    action=lambda: create_task(self.stop_composition()) and None,
                ),
            )
        else:
            items.append(
                ActionItem(
                    key='start-stop',
                    label='Run',
                    icon='󰐊',
                    background_color=SUCCESS_COLOR,
                    action=lambda: create_task(self.run_composition()) and None,
                ),
            )
        items.append(
            ActionItem(
                key='delete',
                label='Delete',
                icon='󰜺',
                background_color=DANGER_COLOR,
                action=self.delete,
            ),
        )

        return items

    def unsubscribe(self: _CompositionItems) -> None:
        self.callback = None

    def subscribe(
        self: _CompositionItems,
        callback: Callable[[list[Item]], None],
    ) -> Callable[[], None]:
        self.callback = callback
        callback(self())
        return self.unsubscribe


def input_docker_composition(*, on_add: Callable[[str], None]) -> None:
    """Input the Docker credentials."""

    async def act() -> None:
        with contextlib.suppress(asyncio.CancelledError):
            _, data = await ubo_input(
                prompt='Import Docker Composition',
                fields=[
                    InputFieldDescription(
                        name='label',
                        label='Label',
                        type=InputFieldType.TEXT,
                        description='The label of this composition',
                        required=True,
                    ),
                    InputFieldDescription(
                        name='yaml',
                        label='Compose YAML',
                        type=InputFieldType.LONG,
                        description='This will be saved as the docker-compose.yml file',
                        required=True,
                    ),
                ],
            )

            if not data or not data['yaml'] or not data['label']:
                return

            id = uuid.uuid4().hex
            composition_path = COMPOSITIONS_PATH / id
            composition_path.mkdir(exist_ok=True, parents=True)
            with (composition_path / 'docker-compose.yml').open('w') as file:
                file.write(data['yaml'])
            with (composition_path / 'label').open('w') as file:
                file.write(data['label'])
            on_add(id)

    create_task(act())


def clear_credentials(registry: str) -> None:
    """Clear an entry in docker credentials."""
    secrets.clear_secret(DOCKER_CREDENTIALS_TEMPLATE.format(registry))
    store.dispatch(DockerRemoveUsernameAction(registry=registry))


@store.autorun(lambda state: state.docker.service.usernames)
def registries_menu_items(usernames: dict[str, str]) -> Sequence[Item]:
    """Get the settings menu items for the Docker service."""
    return [
        ActionItem(
            label='Add Registry',
            icon='󰌉',
            action=input_credentials,
        ),
        *(
            [
                SubMenuItem(
                    label='Registries',
                    icon='󱕴',
                    sub_menu=HeadedMenu(
                        title='󱕴Registries',
                        heading='Logged in Registries',
                        sub_heading='Log out of any registry by selecting it',
                        items=[
                            ActionItem(
                                label=registry,
                                icon='󰌊',
                                background_color=DANGER_COLOR,
                                action=functools.partial(clear_credentials, registry),
                            )
                            for registry in usernames
                        ],
                    ),
                ),
            ]
            if usernames
            else []
        ),
    ]


def _delete_composition(id: str) -> None:
    store.dispatch(DeregisterRegularAppAction(key=id))


def _register_image_app_entry(id: str) -> None:
    if id in IMAGES:
        image = IMAGES[id]
        store.dispatch(
            RegisterRegularAppAction(
                menu_item=ActionItem(
                    label=image.label,
                    icon=image.icon,
                    action=functools.partial(composition_menu, image.id),
                ),
                key=image.id,
            ),
        )
    else:
        path = COMPOSITIONS_PATH / id
        if not path.exists():
            logger.error('Composition not found', extra={'image': id})
            return
        label = (path / 'label').read_text()
        store.dispatch(
            RegisterRegularAppAction(
                menu_item=ActionItem(
                    label=label,
                    icon='󰣆',
                    action=functools.partial(
                        HeadlessMenu,
                        title=label,
                        items=_CompositionItems(
                            path,
                            on_delete=functools.partial(
                                _delete_composition,
                                id,
                            ),
                        ),
                    ),
                ),
                key=id,
            ),
        )


def _load_images() -> None:
    store.dispatch(
        [
            CombineReducerRegisterAction(
                _id=reducer_id,
                key=image_id,
                reducer=image_reducer,
            )
            for image_id in IMAGES
        ],
        [
            CombineReducerRegisterAction(
                _id=reducer_id,
                key=item.stem,
                reducer=image_reducer,
            )
            for item in (
                COMPOSITIONS_PATH.iterdir() if COMPOSITIONS_PATH.is_dir() else []
            )
            if item.stem.startswith('composition_')
        ],
    )


def init_service() -> None:
    """Initialize the service."""
    register_persistent_store(
        'docker_usernames',
        lambda state: state.docker.service.usernames,
    )
    store.dispatch(
        RegisterRegularAppAction(
            menu_item=ActionItem(
                label='Import YAML file',
                icon='󰋺',
                background_color=WARNING_COLOR,
                color='black',
                action=functools.partial(
                    input_docker_composition,
                    on_add=_register_image_app_entry,
                ),
            ),
            key='_import',
        ),
        RegisterSettingAppAction(
            priority=1,
            category=SettingsCategory.DOCKER,
            menu_item=ActionItem(
                label='Service',
                icon='',
                action=setup_menu_action,
            ),
            key='service',
        ),
        RegisterSettingAppAction(
            priority=2,
            category=SettingsCategory.DOCKER,
            menu_item=SubMenuItem(
                label='Registries',
                icon='󱥉',
                sub_menu=HeadedMenu(
                    title='󱥉Docker Registries',
                    heading='󰡨 Docker',
                    sub_heading='Log in to a registry:',
                    items=registries_menu_items,
                ),
            ),
            key='registries',
        ),
    )

    store.subscribe_event(DockerLoadImagesEvent, _load_images)
    store.subscribe_event(
        DockerImageRegisterAppEvent,
        lambda event: _register_image_app_entry(event.image),
    )

    create_task(
        monitor_unit(
            'docker.socket',
            lambda status: store.dispatch(
                DockerSetStatusAction(
                    status=DockerStatus.RUNNING
                    if status in ('active', 'activating', 'reloading')
                    else DockerStatus.NOT_RUNNING,
                ),
            ),
        ),
    )
