from collections import defaultdict


class ModelContext:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelContext, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.context = defaultdict()

        self.default_preprocessor_args = {
            "min_pixels": 4 * 28 * 28,
            "max_pixels": 1280 * 28 * 28,
        }  # TODO: some parameters which are not implemented by openai

        self.context.update(self.default_preprocessor_args)

    def set(self, key, value):
        self.context[key] = value

    def get(self, key):
        return self.context.get(key)


model_contexts = {}


def load_args_into_config(args):
    global model_contexts
    context = ModelContext()
    for key, value in vars(args).items():
        context.set(key, value)
    model_contexts["default"] = context
    return context


def get_model_context(name="default"):
    global model_contexts
    return model_contexts.get(name)


def add_context_args(parser):
    group = parser.add_argument_group("VL Model Engine", "model context")
    group.add_argument("--model", type=str, required=True, help="model name or path")
    group.add_argument(
        "--vision_engine",
        type=str,
        default="tensorrt",
        choices=["tensorrt"],
        help="engine to run vision model",
    )
    group.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda"],
        help="device (Default: cuda)",
    )
    group.add_argument("--max_length", type=int, default=32000, help="model max length")
    group.add_argument("--max_batch", type=int, default=128, help="max batch")
    group.add_argument(
        "--parallel_size",
        type=int,
        default=1,
        help="number of devices used to run engine",
    )
