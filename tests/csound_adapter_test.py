import os
import nose.tools
	
import sound_evolution as se

def setup():
    global simple_json, invalid_json, complex_json, complex_orc
    global csd
    complex_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "complex_instrument.json")).read()
    csd = se.csound_adapter.CSD()
    csd.orchestra(se.instrument.Instrument(complex_json))
    csd.score('i 1 0 2')

def test_play_simple():
    """Should play a simple instrument to sound card."""
    global csd
    csd.play()
    assert os.path.exists(csd.output_csd_filename)
    assert os.path.getsize(csd.output_csd_filename) > 0
    
def test_play_random():
    """Should play a random instrument to sound card."""
    csd_r = se.csound_adapter.CSD()
    csd_r.orchestra(se.instrument.Instrument.random(const_prob=0.7, max_children=4))
    csd_r.score('i 1 0 2')
    csd_r.play()
    assert os.path.exists(csd.output_csd_filename)
    assert os.path.getsize(csd.output_csd_filename) > 0
    
    
def test_render():
    """Should render a given instrument."""
    global csd
    aif_file = "/tmp/__test_out.aif"
    csd.output_aif(aif_file)
    assert os.path.exists(aif_file)
    assert os.path.getsize(aif_file) > 0
