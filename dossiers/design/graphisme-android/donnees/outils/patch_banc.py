import re
p='/tmp/claude-0/releve/android/app/src/test/java/fyi/gildas/callrecorder/BancTest.kt'
s=open(p).read()
s=s.replace("class BancTest {\n", "open class BancTest {\n    open val variante = \"\"\n",1)
old_start=s.index("    private fun image(a: Activity, nom: String")
old_end=s.index("    private fun enCours(trigger: String)")
s=s[:old_start]+'''    protected fun image(a: Activity, nom: String, fond: Int = 0xFFF5F5F5.toInt(), h: Int = 2745) {
        val root = a.findViewById<View>(android.R.id.content)
        val dm = a.resources.displayMetrics
        val night = (a.resources.configuration.uiMode and android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES
        val w = dm.widthPixels
        val hh = if (h == 2745) dm.heightPixels else h * dm.heightPixels / 2745
        root.measure(View.MeasureSpec.makeMeasureSpec(w, View.MeasureSpec.EXACTLY), View.MeasureSpec.makeMeasureSpec(hh, View.MeasureSpec.EXACTLY))
        root.layout(0, 0, w, hh)
        val b = Bitmap.createBitmap(w, hh, Bitmap.Config.ARGB_8888)
        b.eraseColor(if (night) 0xFF1E1E1E.toInt() else fond)
        root.draw(Canvas(b))
        val f = File("build/banc/$variante$nom.png"); f.parentFile.mkdirs()
        f.outputStream().use { b.compress(Bitmap.CompressFormat.PNG, 100, it) }
        val j = File("build/releve/$variante$nom.json"); j.parentFile.mkdirs()
        val out = JSONArray()
        Releve.dump(root, -1, 0, 0, dm.density, a.resources.configuration.fontScale, out)
        j.writeText(JSONObject().put("ecran", nom).put("variante", variante).put("density", dm.density.toDouble()).put("fontScale", a.resources.configuration.fontScale.toDouble())
            .put("night", night).put("wdp", w / dm.density).put("hdp", hh / dm.density).put("vues", out).toString(1))
    }

'''+s[old_end:]
def after(marker, add):
    global s
    i=s.index(marker); j=s.index("\n",i)
    s=s[:j+1]+add+s[j+1:]
after('assertTrue(t, t.contains("Pas encore arrivée sur MacBook Air."))','        image(a, "avant-transcription")\n')
after('assertTrue(t, t.contains("Pas encore transcrite."))','        image(a, "pas-encore-transcrite")\n')
after('assertFalse(t, t.contains("Pas encore transcrite."))','        image(a, "aucune-parole")\n')
after('contains("Rien d\'entendu pour l\'instant."))','        image(a, "direct-rien")\n')
after('        image(a, "conversation")\n','        assertTrue(touche(a.findViewById(android.R.id.content), "Rechercher"))\n        image(a, "conversation-recherche")\n')
# relax the date-dependent assertion of accueil
s=s.replace('assertTrue(t, t.contains("Aujourd\'hui · "))','')
open(p,'w').write(s)
print(s.count('image(a,'))
s=open(p).read()
s=s.replace('''        assertTrue(t, t.contains("Point produit"))
        assertFalse(t, t.contains("Conseil d'école"))
        image(a, "calendrier")''','''        image(a, "calendrier")''')
extra='''
    @Test fun releveAccueilVide() { image(ouvre(), "accueil-vide") }

    @Test fun releveJournal() {
        val a = ouvre() as MainActivity
        a.push(ConversationScreen(a, null))
        image(a, "journal-vide")
    }

    @Test fun releveRecherche() {
        quelquesConversations()
        val a = ouvre()
        assertTrue(touche(a.findViewById(android.R.id.content), "Rechercher"))
        fun champ(v: View): android.widget.EditText? = v as? android.widget.EditText
            ?: (v as? ViewGroup)?.let { g -> (0 until g.childCount).firstNotNullOfOrNull { champ(g.getChildAt(it)) } }
        champ(a.findViewById(android.R.id.content))!!.setText("lundi")
        val fin = System.currentTimeMillis() + 3000
        while (System.currentTimeMillis() < fin && !texte(a.findViewById(android.R.id.content)).contains("occuper")) {
            Thread.sleep(50); org.robolectric.shadows.ShadowLooper.idleMainLooper()
        }
        image(a, "recherche")
    }
}
'''
k=s.rstrip().rindex('}')
s=s[:k]+extra
open(p,'w').write(s)
