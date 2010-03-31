import os
import nose.tools
	
import sound_evolution as se

def setup():
    global csd
    complex_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "complex_instrument.json")).read()
    csd = se.csound_adapter.CSD()
    csd.orchestra(se.instrument.Instrument(complex_json))
    csd.score('i 1 0 2')

def test_play():
    """Should play an instrument to sound card."""
    global csd
    csd.play()
    assert os.path.exists(csd.output_csd_filename)
    assert os.path.getsize(csd.output_csd_filename) > 0

def test_render_aif():
    """Should render aif sound file."""
    global csd
    aif_file = "/tmp/__test_out.aif"
    csd.output_aif(aif_file)
    assert os.path.exists(aif_file)
    assert os.path.getsize(aif_file) > 0
