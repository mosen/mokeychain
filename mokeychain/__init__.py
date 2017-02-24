import sys
import objc
import CoreFoundation

from mokeychain.Security import _metadata

sys.modules['Security'] = mod = objc.ObjCLazyModule('Security',
                                                    "com.apple.security",
                                                    objc.pathForFramework(
                                                        "/System/Library/Frameworks/Security.framework"),
                                                    _metadata.__dict__, None, {
                                                        '__doc__': __doc__,
                                                        '__path__': __path__,
                                                        '__loader__': globals().get('__loader__', None),
                                                        'objc': objc,
                                                    }, (CoreFoundation,))

import sys
# del sys.modules['Security._metadata']
