from enum import Enum
from busline.eventbus.topic import Topic


class CorePluginCommunicationTopic(Enum):
    PLUGIN_DISCOVER = Topic("plugin-discover", description="CORE ---discover---> PLUGIN", content_type="application/json")
    PLUG_OFFER = Topic("plug-offer", description="CORE <---offer--- PLUGIN", content_type="application/json")
    PLUG_REPLY = Topic("plug-reply", description="CORE ---reply---> PLUGIN", content_type="application/json")
    PLUG_OUTCOME = Topic("plug-outcome", description="CORE <---outcome--- PLUGIN", content_type="application/json")