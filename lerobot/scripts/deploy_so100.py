from lerobot.configs.parser import *
from lerobot.scripts.control_robot import *


def no_argv_wrap(config_path: Path | None = None, cli_args: list[str] = None):
    """
    HACK: Similar to draccus.wrap but does three additional things:
        - Will remove '.path' arguments from CLI in order to process them later on.
        - If a 'config_path' is passed and the main config class has a 'from_pretrained' method, will
          initialize it from there to allow to fetch configs from the hub directly
        - Will load plugins specified in the CLI arguments. These plugins will typically register
            their own subclasses of config classes, so that draccus can find the right class to instantiate
            from the CLI '.type' arguments
    """

    def wrapper_outer(fn):
        @wraps(fn)
        def wrapper_inner(*args, **kwargs):
            local_cli_args = cli_args
            argspec = inspect.getfullargspec(fn)
            argtype = argspec.annotations[argspec.args[0]]
            if len(args) > 0 and type(args[0]) is argtype:
                cfg = args[0]
                args = args[1:]
            else:
                # cli_args = sys.argv[1:]
                print("\n", "B"*100, "\n")
                print(local_cli_args, "\n\n\n")
                plugin_args = parse_plugin_args(PLUGIN_DISCOVERY_SUFFIX, local_cli_args)
                for plugin_cli_arg, plugin_path in plugin_args.items():
                    try:
                        load_plugin(plugin_path)
                    except PluginLoadError as e:
                        # add the relevant CLI arg to the error message
                        raise PluginLoadError(f"{e}\nFailed plugin CLI Arg: {plugin_cli_arg}") from e
                    local_cli_args = filter_arg(plugin_cli_arg, local_cli_args)
                config_path_cli = parse_arg("config_path", local_cli_args)
                if has_method(argtype, "__get_path_fields__"):
                    path_fields = argtype.__get_path_fields__()
                    local_cli_args = filter_path_args(path_fields, local_cli_args)
                if has_method(argtype, "from_pretrained") and config_path_cli:
                    local_cli_args = filter_arg("config_path", local_cli_args)
                    cfg = argtype.from_pretrained(config_path_cli, cli_args=local_cli_args)
                else:
                    cfg = draccus.parse(config_class=argtype, config_path=config_path, args=local_cli_args)
            response = fn(cfg, *args, **kwargs)
            return response

        return wrapper_inner

    return wrapper_outer



def deploy(
        fps: int = 30,
        single_task: str = "",
        repo_id: str = "",
        tags: list[str] = None,
        warmup_time_s: int = 5,
        episode_time_s: int = 30,
        reset_time_s: int = 30,
        num_episodes: int = 1,
        push_to_hub: bool = True,
        policy_path: str = ""
):
    bool_str = lambda b: "true" if b else "false"
    @no_argv_wrap(
            cli_args=[
                f"--robot.type=so100",
                f"--control.type=record",
                f"--control.fps={fps}",
                f"--control.single_task={single_task}",
                f"--control.repo_id={repo_id}",
                f"--control.tags={tags}",
                f"--control.warmup_time_s={warmup_time_s}",
                f"--control.episode_time_s={episode_time_s}",
                f"--control.reset_time_s={reset_time_s}",
                f"--control.num_episodes={num_episodes}",
                f"--control.push_to_hub={bool_str(push_to_hub)}",
                f"--control.policy.path={policy_path}"
            ]
    )
    def control_robot(cfg: ControlPipelineConfig):
        init_logging()
        logging.info(pformat(asdict(cfg)))

        # from pprint import pprint
        # print("A"*100, "\n\n")
        # pprint(cfg)
        # print("\n\n", "A"*100)
        # raise

        robot = make_robot_from_config(cfg.robot)

        if isinstance(cfg.control, CalibrateControlConfig):
            calibrate(robot, cfg.control)
        elif isinstance(cfg.control, TeleoperateControlConfig):
            teleoperate(robot, cfg.control)
        elif isinstance(cfg.control, RecordControlConfig):
            record(robot, cfg.control)
        elif isinstance(cfg.control, ReplayControlConfig):
            replay(robot, cfg.control)
        elif isinstance(cfg.control, RemoteRobotConfig):
            from lerobot.common.robot_devices.robots.lekiwi_remote import run_lekiwi

            run_lekiwi(cfg.robot)

        if robot.is_connected:
            # Disconnect manually to avoid a "Core dump" during process
            # termination due to camera threads not properly exiting.
            robot.disconnect()
    
    control_robot()


if __name__ == "__main__":
    cli_args = ['--robot.type=so100', 
                '--control.type=record', 
                '--control.fps=30', 
                '--control.single_task=Grasp a lego block and put it in the bin.', 
                '--control.repo_id=aaaaa/eval_act_so100_test', 
                '--control.tags=["tutorial"]', 
                '--control.warmup_time_s=5', 
                '--control.episode_time_s=30', 
                '--control.reset_time_s=30', 
                '--control.num_episodes=10', 
                '--control.push_to_hub=true', 
                '--control.policy.path=nguyen-v/so100_test_white_plug_pi0']

    deploy(
        single_task="Grasp a lego block and put it in the bin.",
        repo_id="aaaaa/eval_act_so100_test",
        tags='["tutorial"]',
        num_episodes=10,
        policy_path="nguyen-v/so100_test_white_plug_pi0"
    )
