package fyi.gildas.callrecorder

import android.app.AlertDialog
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Typeface
import android.graphics.drawable.ColorDrawable
import android.graphics.drawable.Drawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.RippleDrawable
import android.view.View
import android.view.ViewGroup
import android.widget.Checkable
import android.widget.EditText
import android.widget.TextView
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowLooper
import java.io.File

/**
 * Banc d'inventaire du dossier « UX Android » (design/recos/ux-android). N'appartient pas à l'app : copié dans
 * src/test le temps d'un passage, puis retiré. Chaque état, chaque thème, chaque taille de police : une image et
 * l'arbre des vues (taille, texte, couleur, fond composé, rôle et nom d'accessibilité) dans build/dossier/.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35], qualifiers = "fr-rFR-w412dp-h915dp-xxhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class DossierTest {
    private val c: Context get() = RuntimeEnvironment.getApplication()
    private val now = System.currentTimeMillis()
    private val out = File("build/dossier").also { it.mkdirs() }

    // ---------- Données fictives ----------
    private fun lignes(vararg l: Triple<String, String, Boolean>) = JSONArray().apply {
        l.forEach { (who, text, me) -> put(JSONObject().put("t", "00:${"%02d".format(length() * 7 + 4)}").put("who", who).put("me", me).put("text", text)) }
    }
    private val troisRepliques get() = lignes(
        Triple("Sophie Marchand", "On commence par la feuille de route. Où en est la page des réglages ?", false),
        Triple("Moi", "Elle est prête, il reste les textes à relire.", true),
        Triple("Karim Benali", "Je peux m'en occuper d'ici lundi.", false))

    private fun recue(id: String, title: String, start: Long, minutes: Int, people: List<String>, app: String = "reunion", version: String = "v1", lines: JSONArray = troisRepliques) =
        Conversations.receive(c, JSONObject().put("id", id).put("call", "call-$id").put("app", app).put("title", title).put("start", start)
            .put("end", start + minutes * 60_000L).put("people", JSONArray(people)).put("voices", people.size.coerceAtLeast(2)).put("version", version).put("lines", lines))

    private val h = 3_600_000L
    private fun liste() {
        recue("a1", "Point produit", now - h, 47, listOf("Sophie Marchand", "Karim Benali"))
        recue("a2", "Café avec Thomas", now - 3 * h, 12, listOf("Thomas Girard"), "whatsapp")
        recue("a3", "Paul Mercier · expert-comptable", now - 26 * h, 9, listOf("Paul Mercier"), "android")
        recue("a4", "Conseil d'école", now - 50 * h, 161, emptyList())
        recue("a5", "Claire Duval", now - 74 * h, 12, listOf("Claire Duval"), "signal")
        recue("a6", "Revue mensuelle · Transports Morel", now - 98 * h, 45, listOf("Julie Roussel", "Marc Lefort", "Luc Lefèvre"), "meet")
    }
    private fun enregistre(id: String, trigger: String, debut: Long, app: String? = null) {
        val d = File(c.filesDir, "recordings/$id").also { it.mkdirs() }
        Recordings.writeManifest(d, JSONObject().put("trigger", trigger).put("started", debut).put("ended", debut + 300_000).put("rate", 48_000)
            .put("event", app?.let { JSONObject().put("app", it) } ?: JSONObject.NULL))
        Conversations.keep(c, id)
    }
    private fun enCours(trigger: String) {
        val r = Recordings.Recorder(c, trigger, null, null, {}, {})
        Recordings::class.java.getDeclaredField("current").apply { isAccessible = true }.set(null, r)
    }
    private fun texteDirect() {
        Link.setSpeech(c, true)
        val id = Recordings.current!!.id
        val dossier = c.getExternalFilesDir("transcriptions-google")!!.also { it.mkdirs() }
        File(dossier, "$id.json").writeText(JSONObject().put("started", now).put("chunks", JSONObject()
            .put("0", JSONObject().put("seconds", 60).put("segments", JSONArray().put(JSONObject().put("from", 4.0).put("text", "on commence par le budget"))))
            .put("1", JSONObject().put("segments", JSONArray().put(JSONObject().put("from", 2.0).put("text", "et la suite pour vendredi"))))).toString())
        Speech::class.java.getDeclaredField("changes").apply { isAccessible = true }.setLong(Speech, 1L)
    }

    private fun remiseAZero(lie: Boolean = true) {
        c.filesDir.listFiles()?.forEach { it.deleteRecursively() }
        c.getExternalFilesDir(null)?.listFiles()?.forEach { it.deleteRecursively() }
        for (p in listOf("link", "agenda", "pastille")) c.getSharedPreferences(p, Context.MODE_PRIVATE).edit().clear().commit()
        Recordings::class.java.getDeclaredField("current").apply { isAccessible = true }.set(null, null)
        Recordings.problem = null
        Conversations.apply { javaClass.getDeclaredField("cache").apply { isAccessible = true }.set(this, null) }
        Conversations.journal = null
        Link.wifiHint = null
        Lecteur.forced = true
        android.provider.Settings.Secure.putString(c.contentResolver, android.provider.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES, "")
        if (lie) {
            c.getSharedPreferences("link", Context.MODE_PRIVATE).edit().putString("key", "k").putString("mac", "m").putString("macName", "MacBook Air").commit()
            Link.set(Link.State.READY)
        } else Link.set(Link.State.NEEDS_CODE)
    }

    // ---------- Les états ----------
    private class Etat(val ecran: String, val nom: String, val prepare: () -> Unit, val ouvre: (MainActivity) -> Unit = {})

    private fun cherche(a: MainActivity, mot: String, contenu: Boolean = false) {
        appuie(a, "Rechercher")
        val f = champ(a.findViewById(android.R.id.content))!!
        f.setText(mot)
        val fin = System.currentTimeMillis() + 1500
        while (System.currentTimeMillis() < fin) { Thread.sleep(40); ShadowLooper.idleMainLooper() }
    }

    private val etats: List<Etat> get() = listOf(
        Etat("accueil", "liste", { liste() }),
        Etat("accueil", "vide", {}),
        Etat("accueil", "recherche-ouverte", { liste() }) { appuie(it, "Rechercher") },
        Etat("accueil", "recherche-resultats", { liste() }) { cherche(it, "lundi") },
        Etat("accueil", "recherche-sans-resultat", { liste() }) { cherche(it, "facture") },
        Etat("accueil", "calendrier", { liste() }) { appuie(it, "Calendrier") },
        Etat("accueil", "calendrier-jour-vide", { liste() }) { appuie(it, "Calendrier"); appuie(it, "Mois suivant") },
        Etat("accueil", "enregistrement", { liste(); enCours("main") }),
        Etat("accueil", "enregistrement-appel", { liste(); enCours("appel") }),
        Etat("accueil", "ecoute", { liste(); Link.setListeningSince(c, now - h); enCours("ecoute") }),
        Etat("accueil", "en-attente-du-mac", { liste(); enregistre("p1", "main", now - h / 2) }),
        Etat("accueil", "lien-perdu", { liste(); enregistre("p1", "main", now - h / 2); Link.set(Link.State.SEARCHING) }),
        Etat("conversation", "transcrite-avec-son", {
            liste(); Conversations.sound(c, "a1").writeText("son")
            org.robolectric.shadows.ShadowMediaPlayer.setMediaInfoProvider { org.robolectric.shadows.ShadowMediaPlayer.MediaInfo(47 * 60_000, 0) }
        }) { it.push(ConversationScreen(it, "a1")) },
        Etat("conversation", "transcrite-sans-son", { liste() }) { it.push(ConversationScreen(it, "a3")) },
        Etat("conversation", "longue", {
            recue("l1", "Revue mensuelle · Transports Morel", now - h, 45, listOf("Julie Roussel", "Marc Lefort"), "meet", lines = lignes(
                Triple("Moi", "On a eu quatorze livraisons en retard en octobre, c'est le double de septembre.", true),
                Triple("Julie Roussel", "Je sais. On a perdu deux chauffeurs sur la tournée de Lyon.", false),
                Triple("Marc Lefort", "Et les palettes arrivent mal filmées, on a eu de la casse.", false),
                Triple("Julie Roussel", "Je vous mets un chauffeur dédié sur Lyon dès le 4 novembre.", false),
                Triple("Moi", "Et pour la casse ?", true),
                Triple("Julie Roussel", "On reprend le filmage au quai, et je vous envoie l'avoir d'octobre avant le 15.", false),
                Triple("Marc Lefort", "Il faut aussi qu'ils arrivent avant sept heures, sinon on bloque le quai.", false),
                Triple("Moi", "D'accord. On refait le point dans un mois, même heure.", true)))
        }) { it.push(ConversationScreen(it, "l1")) },
        Etat("conversation", "filtre", { liste() }) { it.push(ConversationScreen(it, "a1")); appuie(it, "Rechercher"); champVisible(it)!!.setText("lundi"); ShadowLooper.idleMainLooper() },
        Etat("conversation", "filtre-sans-resultat", { liste() }) { it.push(ConversationScreen(it, "a1")); appuie(it, "Rechercher"); champVisible(it)!!.setText("budget"); ShadowLooper.idleMainLooper() },
        Etat("conversation", "pas-encore-arrivee", { enregistre("p1", "appel", now - h, "org.telegram.messenger") }) { it.push(ConversationScreen(it, "p1")) },
        Etat("conversation", "pas-encore-transcrite", {
            Conversations.receive(c, JSONObject().put("id", "t1").put("call", "c").put("title", "Point").put("start", now - h).put("end", now - h / 2).put("version", ""))
        }) { it.push(ConversationScreen(it, "t1")) },
        Etat("conversation", "aucune-parole", {
            Conversations.receive(c, JSONObject().put("id", "t1").put("call", "c").put("title", "Point").put("start", now - h).put("end", now - h / 2).put("version", "v1"))
        }) { it.push(ConversationScreen(it, "t1")) },
        Etat("conversation", "en-direct", { liste(); enCours("main"); texteDirect() }) { it.push(ConversationScreen(it, Recordings.current!!.id)); ShadowLooper.idleMainLooper(2, java.util.concurrent.TimeUnit.SECONDS) },
        Etat("conversation", "en-direct-rien", { liste(); enCours("main"); Link.setSpeech(c, true) }) { it.push(ConversationScreen(it, Recordings.current!!.id)) },
        Etat("journal", "sans-reponse-du-mac", { liste(); Link.setListeningSince(c, now - h); enCours("ecoute") }) { it.push(ConversationScreen(it, null)) },
        Etat("journal", "pas-encore-transcrit", { liste(); Link.setListeningSince(c, now - h); enCours("ecoute"); Conversations.journal = emptyList() }) {
            it.push(ConversationScreen(it, null)); Conversations.journal = emptyList(); it.stack().last().render() },
        Etat("journal", "avec-texte", { liste(); Link.setListeningSince(c, now - h); enCours("ecoute") }) {
            it.push(ConversationScreen(it, null))
            Conversations.journal = listOf(Conversations.Line("08:12", "", false, "Bon, je file à la réunion de neuf heures."), Conversations.Line("09:03", "Moi", true, "On commence ?"))
            it.stack().last().render() },
        Etat("reglages", "manuel", { Link.chooseMode(c, "manual") }) { it.push(SettingsScreen(it)) },
        Etat("reglages", "calendrier-sans-calendrier", { Link.chooseMode(c, "agenda") }) { it.push(SettingsScreen(it)) },
        Etat("reglages", "calendrier-du-mac", { Link.chooseMode(c, "agenda"); Link.setCalendar(c, true) }) { it.push(SettingsScreen(it)) },
        Etat("reglages", "tout-le-temps-appels-allumes", {
            Link.chooseMode(c, "active")
            android.provider.Settings.Secure.putString(c.contentResolver, android.provider.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES,
                android.content.ComponentName(c, CallService::class.java).flattenToString())
        }) { it.push(SettingsScreen(it)) },
        Etat("mise-en-route", "aucun-mac", { remiseAZero(lie = false) }),
        Etat("mise-en-route", "sans-google-play", { remiseAZero(lie = false); Lecteur.forced = false }),
        Etat("mise-en-route", "connexion", {
            remiseAZero(lie = false)
            c.getSharedPreferences("link", Context.MODE_PRIVATE).edit().putString("mac", "m").putString("macName", "MacBook Air").commit()
            Link.set(Link.State.CONNECTING)
        }),
        Etat("mise-en-route", "autre-wifi", {
            remiseAZero(lie = false)
            c.getSharedPreferences("link", Context.MODE_PRIVATE).edit().putString("mac", "m").putString("macName", "MacBook Air").commit()
            Link.set(Link.State.SEARCHING); Link.wifiHint = "Maison-5G"
        }),
    )

    private fun MainActivity.stack(): List<Screen> = MainActivity::class.java.getDeclaredField("stack").apply { isAccessible = true }.get(this) as List<Screen>

    // ---------- Gestes ----------
    private fun appuie(a: MainActivity, nom: String): Boolean = appuie(a.findViewById(android.R.id.content), nom)
    private fun appuie(v: View, nom: String): Boolean {
        if (v.visibility != View.VISIBLE) return false
        if (v.contentDescription == nom || (v as? TextView)?.text?.toString()?.substringBefore('\n') == nom) {
            var cible: View? = v
            while (cible != null && !cible.isClickable) cible = cible.parent as? View
            cible?.performClick(); ShadowLooper.idleMainLooper(); return cible != null
        }
        if (v is ViewGroup) for (i in 0 until v.childCount) if (appuie(v.getChildAt(i), nom)) return true
        return false
    }
    private fun champ(v: View): EditText? = v as? EditText ?: (v as? ViewGroup)?.let { g -> (0 until g.childCount).firstNotNullOfOrNull { champ(g.getChildAt(it)) } }
    private fun champVisible(a: MainActivity): EditText? = champVis(a.findViewById(android.R.id.content))
    private fun champVis(v: View): EditText? = if (v.visibility != View.VISIBLE) null else v as? EditText ?: (v as? ViewGroup)?.let { g -> (0 until g.childCount).firstNotNullOfOrNull { champVis(g.getChildAt(it)) } }

    // ---------- Relevé ----------
    private fun couleur(d: Drawable?): Int? = when (d) {
        null -> null
        is ColorDrawable -> d.color
        is GradientDrawable -> d.color?.defaultColor
        is RippleDrawable -> (0 until d.numberOfLayers).firstNotNullOfOrNull { i -> if (d.getId(i) == android.R.id.mask) null else couleur(d.getDrawable(i)) }
        else -> null
    }
    private fun sur(fond: Int, c: Int): Int {
        val a = (c ushr 24) / 255.0
        fun ch(s: Int) = (((c shr s) and 255) * a + ((fond shr s) and 255) * (1 - a)).toInt().coerceIn(0, 255)
        return (0xFF shl 24) or (ch(16) shl 16) or (ch(8) shl 8) or ch(0)
    }
    private fun hex(c: Int) = "#%08X".format(c)

    private fun releve(v: View, root: View, fond: Int, d: Float, sortie: JSONArray, chemin: String) {
        if (v.visibility != View.VISIBLE) return
        var f = fond
        couleur(v.background)?.let { f = sur(fond, it) }
        val xy = IntArray(2); v.getLocationInWindow(xy)
        val rxy = IntArray(2); root.getLocationInWindow(rxy)
        val o = JSONObject()
            .put("chemin", chemin).put("classe", v.javaClass.simpleName)
            .put("x", ((xy[0] - rxy[0]) / d).toDouble()).put("y", ((xy[1] - rxy[1]) / d).toDouble())
            .put("l", (v.width / d).toDouble()).put("h", (v.height / d).toDouble())
            .put("cliquable", v.isClickable).put("actif", v.isEnabled).put("alpha", v.alpha.toDouble())
            .put("fond", hex(f))
            .put("importantA11y", v.importantForAccessibility)
            .put("titreA11y", v.isAccessibilityHeading)
        v.contentDescription?.let { o.put("description", it.toString()) }
        v.stateDescription?.let { o.put("etatA11y", it.toString()) }
        o.put("roleA11y", v.accessibilityClassName?.toString() ?: "")
        if (v is Checkable) o.put("coche", v.isChecked)
        if (v.isSelected) o.put("choisi", true)
        if (v is TextView) {
            o.put("texte", v.text.toString()).put("taillePx", v.textSize.toDouble()).put("tailleSp", (v.textSize / v.resources.displayMetrics.scaledDensity).toDouble())
                .put("tailleDp", (v.textSize / d).toDouble())
                .put("couleurTexte", hex(v.currentTextColor)).put("gras", (v.typeface?.isBold == true) || (v.typeface?.weight ?: 400) >= 500 || v.typeface == Typeface.create("sans-serif-medium", Typeface.NORMAL))
                .put("graisse", v.typeface?.weight ?: 400)
            if (v is EditText) o.put("indice", v.hint?.toString() ?: "").put("couleurIndice", hex(v.currentHintTextColor))
            v.layout?.let { lay ->
                var coupe = 0
                for (i in 0 until lay.lineCount) coupe += lay.getEllipsisCount(i)
                o.put("lignes", lay.lineCount).put("points", coupe)
                    .put("hauteurTexte", (lay.height / d).toDouble())
                    .put("debordeVertical", lay.height + v.totalPaddingTop + v.totalPaddingBottom > v.height + 1)
                    .put("debordeHorizontal", (0 until lay.lineCount).any { lay.getLineWidth(it) > (v.width - v.totalPaddingLeft - v.totalPaddingRight) + 1 })
            }
        }
        sortie.put(o)
        if (v is ViewGroup) for (i in 0 until v.childCount) releve(v.getChildAt(i), root, f, d, sortie, "$chemin/${i}")
    }

    private fun capture(root: View, nom: String, l: Int, h: Int, fond: Int) {
        root.measure(View.MeasureSpec.makeMeasureSpec(l, View.MeasureSpec.EXACTLY), View.MeasureSpec.makeMeasureSpec(h, View.MeasureSpec.EXACTLY))
        root.layout(0, 0, l, h)
        val b = Bitmap.createBitmap(l, h, Bitmap.Config.ARGB_8888)
        b.eraseColor(fond)
        root.draw(Canvas(b))
        File(out, "$nom.png").outputStream().use { b.compress(Bitmap.CompressFormat.PNG, 100, it) }
        val d = root.resources.displayMetrics.density
        val vues = JSONArray()
        releve(root, root, fond, d, vues, "")
        File(out, "$nom.json").writeText(JSONObject().put("nom", nom).put("densite", d.toDouble()).put("echellePolice", root.resources.configuration.fontScale.toDouble())
            .put("vues", vues).toString(1))
    }

    private fun tout(theme: String, police: Float) {
        RuntimeEnvironment.setQualifiers(if (theme == "sombre") "+night" else "+notnight")
        RuntimeEnvironment.setFontScale(police)
        val suffixe = "$theme-${(police * 100).toInt()}"
        for (e in etats) {
            remiseAZero()
            e.prepare()
            val a = Robolectric.buildActivity(MainActivity::class.java).setup().get()
            ShadowLooper.idleMainLooper()
            try { e.ouvre(a) } catch (x: Throwable) { File(out, "erreurs.txt").appendText("${e.ecran}-${e.nom} $suffixe : $x\n") }
            ShadowLooper.idleMainLooper()
            capture(a.findViewById(android.R.id.content), "${e.ecran}--${e.nom}--$suffixe", 1236, 2745, a.look.background)
        }
        // Les boîtes de dialogue (Android les dessine, l'app en écrit les mots).
        dialogues(suffixe)
        // La pastille.
        remiseAZero()
        val p = Pastille(c, {}, {})
        val v = p.view
        v.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        capture(v, "pastille--seule--$suffixe", v.measuredWidth, v.measuredHeight, 0xFF8899AA.toInt())
    }

    private fun dialogues(suffixe: String) {
        val liste = JSONArray()
        fun garde(nom: String) {
            ShadowLooper.idleMainLooper()
            val dlg = ShadowAlertDialog.getLatestAlertDialog() ?: return
            val sh = org.robolectric.Shadows.shadowOf(dlg)
            val o = JSONObject().put("nom", nom).put("titre", sh.title?.toString() ?: "").put("message", sh.message?.toString() ?: "")
            for ((k, b) in listOf("positif" to AlertDialog.BUTTON_POSITIVE, "neutre" to AlertDialog.BUTTON_NEUTRAL, "negatif" to AlertDialog.BUTTON_NEGATIVE))
                dlg.getButton(b)?.takeIf { it.visibility == View.VISIBLE && it.text.isNotEmpty() }?.let { o.put(k, it.text.toString()).put("$k-couleur", hex(it.currentTextColor)) }
            liste.put(o)
            val deco = dlg.window!!.decorView
            capture(deco, "dialogue--$nom--$suffixe", 1236, (deco.height.takeIf { it > 0 } ?: 1200), 0xFF808080.toInt())
            dlg.dismiss()
        }
        remiseAZero(); liste()
        var a = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        a.push(ConversationScreen(a, "a1")); appuie(a, "Détails"); garde("details")
        appuie(a, "Plus"); ShadowLooper.idleMainLooper()
        org.robolectric.shadows.ShadowPopupMenu.getLatestPopupMenu()?.let { m ->
            liste.put(JSONObject().put("nom", "menu-plus").put("entrees", JSONArray((0 until m.menu.size()).map { m.menu.getItem(it).title.toString() })))
            org.robolectric.Shadows.shadowOf(m).onMenuItemClickListener.onMenuItemClick(m.menu.getItem(0))
        }
        garde("supprimer")
        remiseAZero(); liste(); enregistre("p1", "main", now - h / 2)
        a = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        a.push(ConversationScreen(a, "p1")); appuie(a, "Plus"); ShadowLooper.idleMainLooper()
        org.robolectric.shadows.ShadowPopupMenu.getLatestPopupMenu()?.let { m -> org.robolectric.Shadows.shadowOf(m).onMenuItemClickListener.onMenuItemClick(m.menu.getItem(0)) }
        garde("supprimer-pas-encore-arrivee")
        remiseAZero()
        a = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        a.push(SettingsScreen(a)); appuie(a, "Enregistrer les appels"); garde("appels")
        appuie(a, "Mac, MacBook Air"); garde("mac-connecte")
        remiseAZero(); enregistre("p1", "main", now - h / 2); enregistre("p2", "main", now - h); Link.set(Link.State.SEARCHING)
        a = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        a.push(SettingsScreen(a)); appuie(a, "Mac, MacBook Air"); garde("mac-injoignable-deux-en-attente")
        remiseAZero(); Link.setCalendar(c, true)
        a = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        a.push(SettingsScreen(a)); appuie(a, "Calendrier, MacBook Air"); garde("calendrier-du-mac")
        File(out, "dialogues--$suffixe.json").writeText(liste.toString(1))
    }

    @Test fun clair100() = tout("clair", 1.0f)
    @Test fun clair130() = tout("clair", 1.3f)
    @Test fun clair200() = tout("clair", 2.0f)
    @Test fun sombre100() = tout("sombre", 1.0f)
    @Test fun sombre130() = tout("sombre", 1.3f)
    @Test fun sombre200() = tout("sombre", 2.0f)
}
