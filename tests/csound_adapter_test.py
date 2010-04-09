import os, re
import nose.tools

import sound_evolution as se

def setUp():
    global csd, aif_filename, tone_json
    aif_filename = "/tmp/__test_out.aif"
    tone_json = open(
        os.path.join(os.path.dirname(__file__),
                     "fixtures", "20kHz_tone.json")).read()
    csd = se.csound_adapter.CSD()
    csd.orchestra(se.instrument.Instrument(tone_json))
    csd.score('i 1 0 2')

def test_play():
    """Should play an instrument to sound card."""
    global csd
    csd.play()
    assert re.search("PortAudio: selected output device",
                     csd.last_run_output)
    assert re.search("\d+-byte soundblks of shorts written to dac",
                     csd.last_run_output)
    assert os.path.exists(csd.output_csd_filename)
    assert os.path.getsize(csd.output_csd_filename) > 0

def test_render_aif():
    """Should render aif sound file."""
    global csd, aif_filename
    csd.output_aif(aif_filename)
    assert re.search("\d+-byte soundblks of shorts written to %s" % aif_filename,
                     csd.last_run_output)
    assert os.path.exists(aif_filename)
    assert os.path.getsize(aif_filename) > 0

def test_clean_tmp_files():
    """Should clean up temp files."""
    global aif_filename, tone_json
    # This test uses its own instance of CSD since other tests would
    # fail without the object.
    csd = se.csound_adapter.CSD()
    csd.orchestra(se.instrument.Instrument(tone_json))
    csd.score('i 1 0 2')
    csd.output_aif(aif_filename)
    csd_filename = csd.output_csd_filename
    del csd
    assert not os.path.exists(aif_filename)
    assert not os.path.exists(csd_filename)

@nose.tools.raises(OSError)
def test_fail_without_csound():
    """Should fail without csound binary"""
    global csd
    csd.csound_binary = "/this/path/for/sure/does/not/exists/csound"
    csd.play()
