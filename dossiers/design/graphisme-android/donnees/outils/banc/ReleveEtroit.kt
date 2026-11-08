package fyi.gildas.callrecorder
import org.robolectric.annotation.Config
@Config(sdk = [35], qualifiers = "fr-rFR-w360dp-h780dp-xxhdpi")
class ReleveEtroit : BancTest() { override val variante = "etroit/" }
