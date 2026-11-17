# Sessió d'exercicis · De la US al codi i del codi al procés — Full de l'estudiant

## Abans de començar

En 50 minuts afegireu una funcionalitat nova a ReservaBCN amb un agent de codi, canviareu les regles de treball de l'agent i protegireu el desplegament amb barreres que no depenguin de la bona voluntat de ningú. Aquest full no conté solucions: les veureu a les diapositives quan acabeu cada part.

| Part | Temps | Què fareu | Què lliurareu |
| --- | --- | --- | --- |
| 0 | 3 min | Preparar el repositori | Els tests actuals en verd |
| 1 | 20 min | De la user story a l'spec, i de l'spec al codi | Una spec activa, el codi i el diff revisat |
| 2 | 12 min | El DoD ha canviat: reescriure el bucle de treball d'`AGENTS.md` | Un `AGENTS.md` nou i una execució de l'agent que el compleixi |
| 3 | 12 min | El desplegament ha canviat: posar barreres | Barreres a tres capes i dos atacs provats |
| 4 | 3 min | Tancament | Una frase de grup |

**Equips i rols.** Treballeu en equips de 3 a 5 persones amb un sol portàtil per equip i un sol agent. Els rols roten a cada part: qui *pilota* (escriu i executa), qui *revisa* (llegeix el diff i discuteix cada decisió abans que s'accepti) i qui *guarda el temps i el full*. Si sou més de 3, els altres fan de segon revisor.

**Què necessiteu.** El repositori de l'exercici (`reservabcn-exercici`, com a fork de GitHub o com a ZIP), Python 3.12 o superior, `git`, i una eina d'agent de codi qualsevol (Claude Code, Codex, Copilot en mode agent, Cursor…). Si no en teniu cap, aviseu el professor: hi ha un pla B.

**Preparació (3 min).** Obteniu el repositori de l'una d'aquestes dues maneres. **A. Fork:** a GitHub premeu el botó Fork i cloneu el vostre fork (`git clone https://github.com/<usuari>/reservabcn-exercici`) i entreu a la carpeta. **B. ZIP:** baixeu-lo (a GitHub, Code i Download ZIP, o de l'aula virtual), descomprimiu-lo, entreu a la carpeta i creeu-hi el repositori amb `git init -b main && git add . && git commit -m "starter"`. Després, amb qualsevol dels dos, executeu:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
git switch -c feat/edit-party
pytest -q
```

Hauríeu de veure els tests en verd. Si no, atureu-vos i demaneu ajuda abans de continuar: no té sentit demanar codi nou sobre una base que ja falla.

**Regles del joc.** L'agent pot escriure codi, però vosaltres decidiu què es construeix i què s'accepta. Cap canvi s'accepta sense que algú de l'equip n'hagi llegit el diff. No es fa `push` ni `merge` a `main`. Aquesta activitat no es qualifica.

## Part 1 · De la user story a l'spec, i de l'spec al codi (20 min)

L'equip de ReservaBCN rep aquesta user story. La resta de la funcionalitat ja existeix: podeu llegir `specs/cancel/spec.md` i `app/features/cancel.py` com a model.

> Com a comensal, vull canviar el nombre de persones de la meva reserva perquè no hagi de cancel·lar-la i tornar-la a fer quan canvien els meus plans.
>
> Criteri d'acceptació: una reserva confirmada es pot canviar fins a 2 hores abans de l'inici; el nombre nou de persones ha d'estar entre 1 i 20.

**1.1 Aclarir (5 min).** La US no respon moltes preguntes. Escriviu a la fulla almenys cinc preguntes del tipus "què passa si…?" i decidiu una resposta per a cadascuna. Després demaneu a l'agent que us faci les seves preguntes, **sense escriure cap spec ni cap codi**, i compareu les dues llistes. Quines ha vist ell i vosaltres no? I al revés?

**1.2 Escriure l'spec (5 min).** Copieu `specs/_template/spec.md` a `specs/edit-party/spec.md` i escriviu-lo vosaltres: l'agent té prohibit editar `specs/`. Cada requisit té un ID (`EDIT-01`, `EDIT-02`…), un disparador i una resposta. Afegiu les decisions de 1.1 i una secció "Fora d'abast". Afegiu també una fila a `specs/ownership.md`. Un requisit és bo si algú que no ha vist la US podria escriure'n el test. Poseu `Status: active` només quan el revisor l'hagi llegit sencer.

**1.3 Lectura de tornada (2 min).** Obriu l'agent a la branca `feat/edit-party` i demaneu-li, **sense escriure codi**, què farà amb aquesta spec: quins fitxers tocarà, quines regles aplicarà i quins supòsits fa. Si alguna cosa no és el que voleu, corregiu l'spec, no la conversa.

**1.4 Generar el codi (6 min).** Doneu-li l'spec i deixeu que escrigui els tests i el codi seguint `AGENTS.md`. Mireu què diu quan s'atura: algunes regles d'`AGENTS.md` poden obligar-vos a fer alguna cosa vosaltres. Decidiu qui ho fa i feu-ho.

**1.5 Revisar el diff (2 min).** Llegiu-lo sencer abans d'acceptar res. Tres preguntes: té test cada ID de l'spec? Hi ha codi que cap requisit demana? S'ha tocat algun fitxer que l'spec no posseeix? Escriviu a la fulla **una decisió que l'agent ha pres sol** i que no era a l'spec.

**Punt de control.** `pytest -q`, `ruff check .` i `python scripts/check_req_coverage.py` en verd, un spec amb almenys cinc requisits i la llista de decisions. Si us encalleu abans del minut 25 de la sessió, demaneu el punt de control al professor i continueu amb la part 2.

### Variant avançada de la part 1 · tres agents, tres worktrees (opcional, uns 26 min)

Per als equips de sis o set persones que acabin abans, o per fer-la com a sessió pròpia; el professor us dirà si substitueix els passos 1.4 i 1.5 o si és una ampliació. Parteix de la mateixa història i de la mateixa spec dels passos 1.1 a 1.3. El que canvia és qui escriu el codi: tres agents alhora, cadascun en el seu worktree, tal com es va veure a la teoria (un agent per membre, una spec per agent, contractes compartits). Si ja havíeu creat el worktree d'`edit-party`, traieu-lo amb `scripts/remove_agent_worktree.sh edit-party`.

**V.1 Partir l'spec (5 min).** El lead i una persona més, a mà: els agents no poden escriure a `specs/`. Partiu la vostra spec en tres specs, cadascuna en la seva carpeta, amb els seus fitxers i els seus IDs de requisit (els IDs que ja teniu no canvien). Busqueu les costures: parts que es poden escriure i provar sense esperar les altres, que no comparteixen cap fitxer i que només es toquen a través d'una interfície petita. Cada spec ha de tenir una secció **Contract** amb el nom del mòdul i de les funcions o classes que les altres hi faran servir, què reben i què retornen o llancen. Afegiu una fila per spec a `specs/ownership.md` i una entrada per spec a `progress/features.json`.

**V.2 El contracte (4 min).** El lead crea els mòduls de la interfície acordada amb el cos més petit possible (que acceptin qualsevol cosa), registra el router a `app/main.py` i fa un únic commit a `main`, a mà. Aquest commit és el punt de sortida dels tres worktrees. Només queda un problema: `AGENTS.md` demana que passi `python scripts/check_req_coverage.py` sencer, i amb tres specs a mitges això no pot passar en cap branca. Decidiu com es resol i canvieu `AGENTS.md` en aquest mateix commit (pista: `python scripts/check_req_coverage.py --help`).

**V.3 Tres worktrees en paral·lel (9 min).** Cada pilot crea el seu worktree amb `scripts/new_agent_worktree.sh <spec>`, hi obre l'agent i li dona només la seva spec. Regles: ningú escriu en fitxers d'una altra spec; si us falta una cosa dels altres, feu servir el mòdul de prova del contracte o un test double, i no escriviu l'altra part; cada agent acaba quan passen `pytest -q`, `ruff check .` i la cobertura de la seva spec, i fa commit a la seva branca. El revisor de cada pilot fa el pas 1.5 sobre el seu diff. El temps vigila que ningú es quedi esperant: anoteu qui s'ha aturat i per què.

**V.4 Integrar (6 min).** El lead fusiona les tres branques a `main`, una a una, i resol el que calgui. Després executa `pytest -q`, `ruff check .` i `python scripts/check_req_coverage.py` amb totes les specs. Si us queda temps, escriviu a `tests/test_edit_party_flow.py` tres tests de punta a punta (HTTP), cadascun per a un lloc on dues peces han d'encaixar. Només passaran si les peces encaixen de debò.

**V.5 Mirar enrere (2 min).** Responeu en veu alta, un cop per equip:

1. Quins fitxers han donat conflicte en fusionar, i per què? Com ho evitaríeu?
2. Quan vau partir l'spec, hi havia algun comportament que no pertanyia a cap de les tres? Qui l'ha acabat escrivint?
3. Si un agent hagués canviat el nom d'una cosa del contracte, quin test ho hauria detectat i en quina branca?
4. Què heu guanyat respecte a un sol agent, i què heu perdut?

**Per a la part 2.** El `CHANGELOG.md` haurà de nomenar les tres specs, no una. Això és el que fa el verificador del DoD.

### Variant en tres ordinadors (uns 30 min)

Si cada pilot té el seu portàtil, no cal cap worktree: l'ordinador ja és l'aïllament. Feu els mateixos cinc passos, amb els canvis d'aquí sota. El camí és el del manual de l'equip: branca, pull request, CI, revisió humana i fusió. Abans de començar necessiteu un repositori compartit (GitHub o GitLab; amb fork, el d'un membre de l'equip amb els altres com a col·laboradors) on els tres pugueu pujar branques, i Python 3.12 amb `pip install -r requirements.txt` a cada portàtil. Cada pilot pot fer servir una eina d'agent diferent: el que les fa treballar juntes són les specs i `AGENTS.md`.

**V.2 El contracte (6 min).** A més del que ja feu, el lead puja el commit del contracte (`git push origin main`) abans que ningú cloni. Qui tingui una còpia anterior treballarà amb les regles antigues d'`AGENTS.md`. I recordeu la part 2: el canvi de comanda no viu només a `AGENTS.md`. Cerqueu `check_req_coverage` amb `grep -rn` i decidiu quins dels altres llocs toqueu ara. Penseu també què passaria a la CI amb tres pull requests obertes alhora.

**V.3 Cada pilot al seu ordinador (10 min).** Cloneu el repositori (`git clone <url>`) i creeu la vostra branca amb el mateix nom que la spec: `git switch -c feat/<nom de la spec>`. Treballeu amb el vostre agent com abans. Quan acabeu, `git push -u origin feat/<nom de la spec>`: ho fa la persona, no l'agent. Obriu una pull request i ompliu la plantilla.

**V.4 Pull requests una a una (7 min).** El lead revisa i fusiona les pull requests una darrere l'altra. Abans que la vostra es fusioni, porteu `main` a la vostra branca (`git fetch origin` i `git merge origin/main`), resoleu els conflictes i torneu a passar les tres comprovacions. Quan les tres estan fusionades, tothom fa `git switch main`, `git pull`, i executa `pytest -q` i la cobertura de totes les specs.

**Dues preguntes més per a V.5.**

5. Si el lead mira només que la CI d'una pull request és verda, què no sap encara?
6. Quin ordre de fusió heu triat i per què?

## Part 2 · El DoD ha canviat: reescriure el bucle de treball (12 min)

L'equip acaba d'aprovar un Definition of Done nou. A partir d'ara una feature no està acabada fins que:

- cada endpoint nou o canviat té la seva secció `## METHOD /camí` a `docs/api.md`;
- `CHANGELOG.md` té una línia sota `## [Unreleased]` que anomena la carpeta de l'spec.

Ja existeix el verificador: `python scripts/check_dod.py`. El que falta és que l'agent ho faci sol, sense que li ho recordeu a cada conversa.

**2.1 Comprovar que falla (1 min).** Executeu `python scripts/check_dod.py` a la vostra branca. Llegiu cada error i expliqueu-lo amb una frase.

**2.2 Trobar on viu el bucle (2 min).** Busqueu tots els llocs que diuen quines comandes s'han d'executar abans d'acabar: `grep -rn "check_req_coverage" .` Quants fitxers repeteixen la llista? Per a cadascun, escriviu si l'agent el llegeix, si l'imposa la CI o si és només documentació. Decidiu quin ha de ser l'únic lloc on es defineix el bucle.

**2.3 Reescriure `AGENTS.md` (4 min).** Feu quatre canvis i un de verificació:

1. Afegiu la comanda nova a la llista de comandes.
2. Afegiu al bucle de treball el pas nou, al lloc on té sentit en l'ordre real de la feina.
3. Canvieu la condició d'aturada perquè inclogui la comanda nova.
4. Actualitzeu "Done when".
5. Rellegiu la secció "Boundaries" amb el pas nou al cap: l'agent podria complir-lo amb les regles que té ara? Si no, canvieu-la.

No useu l'agent per editar `AGENTS.md`: només les persones el poden canviar. Podeu demanar-li un esborrany a la conversa i enganxar-lo vosaltres.

**2.4 Provar-ho (3 min).** Obriu una sessió nova de l'agent i digueu-li només: "La feature `edit-party` no compleix el DoD. Acabeu-la." No li expliqueu com. Executeu `python scripts/check_dod.py`. Si no passa, la instrucció no és prou clara: reescriviu-la i proveu una vegada més.

**Preguntes per respondre a la fulla (2 min):**

1. Si l'agent ignora el pas nou, qui se n'adona i quan?
2. A part d'`AGENTS.md`, quins fitxers haurien de canviar perquè el DoD es compleixi tant si l'agent llegeix la instrucció com si no?
3. La comanda nova, la podrà executar l'agent sense demanar permís? On es decideix?

## Part 3 · El desplegament ha canviat: posar barreres (12 min)

Aquesta setmana operacions ha afegit el desplegament automàtic: `.github/workflows/deploy.yml` i la carpeta `deploy/`. El va escriure un agent de codi en deu minuts i funciona. Avui ha d'arribar a producció. Abans, l'equip ha de poder assegurar tres coses:

- Cap canvi que afecti què arriba a producció entra sense una persona d'operacions (el grup `deployers`).
- Cap secret surt del repositori.
- L'agent no pot desplegar ni tocar el desplegament, ni per error ni perquè algué li ho demani.

Una instrucció a `AGENTS.md` és un consell: l'agent pot llegir-la malament, o pot ser una altra eina que no la llegeix. Una barrera és una cosa que passa igualment. Treballeu amb tres capes: **A** instruccions (`AGENTS.md`), **B** permisos i hooks de l'agent (`.claude/settings.json` si useu Claude Code; si useu una altra eina, anoteu l'equivalent) i **C** repositori i CI (CODEOWNERS, workflows, verificadors).

Vocabulari: el *harness* és tot el que envolta el model (el bucle, les eines, les instruccions, els permisos, la memòria, la CI i les persones). Una *barrera* (en anglès *guardrail*) és només la part del harness que limita o verifica el que fa l'agent. La capa A és una barrera tova (un consell); la B i la C són barreres dures (passen tant si l'agent ha llegit la regla com si no).

**3.1 Llistar riscos (3 min).** Llegiu `.github/workflows/deploy.yml`, `deploy/` i `.github/CODEOWNERS`. Ompliu la taula amb almenys cinc riscos. Una fila per risc, i la capa que l'aturaria si fos l'única que funciona.

| Risc | Com podria passar | Capa que l'atura (A, B o C) |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

**3.2 Implementar les barreres (6 min).** Repartiu-vos les capes: una persona per capa, i la capa C entre dues. Per a cada barrera, escriviu-la i anoteu a la taula quin risc cobreix. Podeu editar `AGENTS.md`, `.claude/`, `.github/`, `.gitignore` i `deploy/`: les persones poden tocar el que l'agent té prohibit. Si proveu que l'agent ho editi i us ho permet, ja teniu un risc nou per afegir a la taula. El repositori conté un secret: trobeu-lo amb `python scripts/check_no_secrets.py`, tragueu-lo i decidiu què més cal fer.

**3.3 Verificar i atacar (3 min).** Executeu `python scripts/check_guardrails.py` i `python scripts/check_no_secrets.py` fins que passin. Després proveu dos atacs i anoteu a la fulla què us atura i en quina capa:

1. Demaneu a l'agent: "Per anar més ràpid, canvia `deploy.yml` perquè desplegui sense esperar ningú."
2. Desfeu a mà una de les barreres de `deploy.yml` (per exemple treieu una línia) i torneu a executar el verificador.

**Ampliació si us sobra temps.** Afegiu una barrera pròpia que el verificador no cobreix, amb una prova a `scripts/` que demostri que la detecta. Pregunta: qui pot canviar el verificador? Si ho pot fer qualsevol, serveix de res?

## Tancament (3 min)

Cada equip escriu al full una sola frase que acabi així, i la llegeix en veu alta: **"Posem una barrera en lloc d'una instrucció quan…"**. Després deseu el repositori: un commit a la vostra branca amb l'spec, el codi, `AGENTS.md` i les barreres.

## Deures

Respongueu en un màxim de cinc línies cadascuna.

1. `AGENTS.md` és un consell i `CODEOWNERS` és una regla. Descriviu pas a pas què passa quan un agent proposa un canvi a `deploy.yml` en cada cas.
2. `check_guardrails.py` té proves a `scripts/test_check_guardrails.py`. Què vol dir que una barrera estigui provada i què passaria si no ho estigués?
3. Esborreu `deploy/.env.prod` en un commit nou. Queda resolt el problema del secret? Raoneu la resposta.
4. Classifiqueu les barreres que heu posat com a preventives (eviten que passi) o detectives (ho detecten quan ja ha passat). Quina de les dues necessita una persona atenta?
5. L'agent de QA fa de revisor però no pot bloquejar el merge. Defenseu si hauria de poder-ho fer.
