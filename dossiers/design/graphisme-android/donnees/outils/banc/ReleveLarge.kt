package fyi.gildas.callrecorder
import org.robolectric.annotation.Config
@Config(sdk = [35], qualifiers = "fr-rFR-w600dp-h960dp-xxhdpi")
class ReleveLarge : BancTest() { override val variante = "large/" }
