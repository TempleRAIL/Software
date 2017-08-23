from duckietown_utils.path_utils import expand_all, display_filename
import cPickle
from duckietown_utils import logger
import os



def get_cached(cache_name, f):
    """ 
        Caches the result of f() in a file called
            ${DUCKIETOWN_ROOT}/caches/![name].cache.pickle
    """
            
    cache = '${DUCKIETOWN_ROOT}/caches/%s.cache.pickle' % cache_name
    cache = expand_all(cache)
    
    if os.path.exists(cache):
        logger.info('Using cache %s' % display_filename(cache))
        with open(cache) as f:
            ob = cPickle.load(f)
    else:
        ob = f()
        logger.info('Writing to cache %s' % display_filename(cache))
        try:
            os.makedirs(os.path.dirname(cache))
        except:
            pass
        with open(cache, 'w') as f:
            cPickle.dump(ob, f)
    return ob
