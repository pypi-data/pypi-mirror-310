
from .bark import BarkDeploy
from .chattts import ChatTTSDeploy
from .musicgen import MusicGenDeploy

class TTSDeploy:
    """TTSDeploy is a factory class for creating instances of different Text-to-Speech (TTS) deployment types based on the specified name.

`__new__(cls, name, **kwarg)`
The constructor dynamically creates and returns the corresponding deployment instance based on the provided name argument.

Args: 
    name: A string specifying the type of deployment instance to be created.
    **kwarg: Keyword arguments to be passed to the constructor of the corresponding deployment instance.
                
Returns:
    If the name argument is 'bark', an instance of [BarkDeploy][lazyllm.components.BarkDeploy] is returned.
    If the name argument is 'ChatTTS', an instance of [ChatTTSDeploy][lazyllm.components.ChatTTSDeploy] is returned.
    If the name argument starts with 'musicgen', an instance of [MusicGenDeploy][lazyllm.components.MusicGenDeploy] is returned.
    If the name argument does not match any of the above cases, a RuntimeError exception is raised, indicating the unsupported model.            


Examples:
    >>> from lazyllm import launchers, UrlModule
    >>> from lazyllm.components import TTSDeploy
    >>> model_name = 'bark'
    >>> deployer = TTSDeploy(model_name, launcher=launchers.remote())
    >>> url = deployer(base_model=model_name)
    >>> model = UrlModule(url=url)
    >>> res = model('Hello World!')
    >>> print(len(res), res[:50])
    ... 387355 {"lazyllm_sounds": [24000, [-111.9375, -106.4375, -106.875
    """

    def __new__(cls, name, **kwarg):
        if name == 'bark':
            return BarkDeploy(**kwarg)
        elif name == 'ChatTTS':
            return ChatTTSDeploy(**kwarg)
        elif name.startswith('musicgen'):
            return MusicGenDeploy(**kwarg)
        else:
            raise RuntimeError(f"Not support model: {name}")
