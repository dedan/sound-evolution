import os
import nose.tools
	
import sound_evolution as se

def setup():
    global simple_json, invalid_json, complex_json, complex_orc
    complex_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "complex_instrument.json")).read()

def test_sound():
    """Should play/render a given/random instrument."""
    random = 1 # 0=no, 1=yes
    render = 0 # 0=no, 1=yes

    csd_file = "__test_out.csd"
    aif_file = "__test_out.aif"
            
    if random:
        params = {"const_prob": 0.7, "max_children": 4}
        i = se.instrument.Instrument.random(params)
    else:
        global complex_json
        i = se.instrument.Instrument(complex_json)        

    csd = se.csound_adapter.CSD(csd_file, render)
    csd.orchestra(i)
    csd.score('i 1 0 2')
    csd.output(csd_file)
    
    assert(os.path.exists(csd_file))
    assert(os.path.getsize(csd_file) > 0)
    if render:
        assert(os.path.exists(aif_file))
        assert(os.path.getsize(aif_file) > 0)
    
