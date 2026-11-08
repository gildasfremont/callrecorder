package fyi.gildas.callrecorder
import org.junit.Before
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
@Config(sdk = [35], qualifiers = "fr-rFR-w412dp-h915dp-xxhdpi")
class ReleveTexte200 : BancTest() {
    override val variante = "texte200/"
    @Before fun grand() { RuntimeEnvironment.setFontScale(2.0f) }
}
