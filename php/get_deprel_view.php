<?php 

include ('connexion.php');
include("start_session.php");

if(!(isset($_SESSION) && isset($_SESSION["user_id"]) && isset($_GET["document"]))){
    print "<br/>Required tokens were not provided. Aborting.<br/>";
    http_response_code(400);
    exit;
}

?>


<div class="conllu-parse" tabs="yes" style="width: 1000px;">
# generator = UDPipe 2, https://lindat.mff.cuni.cz/services/udpipe
# udpipe_model = french-gsd-ud-2.10-220711
# udpipe_model_licence = CC BY-NC-SA
# newdoc
# newpar
# sent_id = 1
# text = Pendant plusieurs jours de suite des lambeaux d'armée en déroute avaient traversé la ville.
1	Pendant	pendant	ADP	_	_	3	case	_	SpacesBefore=\s\s\s|TokenRange=3:10
2	plusieurs	plusieurs	DET	_	Number=Plur|PronType=Ind	3	det	_	TokenRange=11:20
3	jours	jour	NOUN	_	Gender=Masc|Number=Plur	14	obl:mod	_	TokenRange=21:26
4	de	de	ADP	_	_	5	case	_	TokenRange=27:29
5	suite	suite	NOUN	_	Gender=Fem|Number=Sing	3	nmod	_	TokenRange=30:35
6-7	des	_	_	_	_	_	_	_	TokenRange=36:39
6	de	de	ADP	_	_	8	case	_	_
7	les	le	DET	_	Definite=Def|Number=Plur|PronType=Art	8	det	_	_
8	lambeaux	lambeau	NOUN	_	Gender=Masc|Number=Plur	3	nmod	_	TokenRange=40:48
9	d'	de	ADP	_	_	10	case	_	SpaceAfter=No|TokenRange=49:51
10	armée	armée	NOUN	_	Gender=Fem|Number=Sing	8	nmod	_	TokenRange=51:56
11	en	en	ADP	_	_	12	case	_	TokenRange=57:59
12	déroute	déroute	NOUN	_	Gender=Fem|Number=Sing	8	nmod	_	TokenRange=60:67
13	avaient	avoir	AUX	_	Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin	14	aux:tense	_	TokenRange=68:75
14	traversé	traverser	VERB	_	Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part	0	root	_	TokenRange=76:84
15	la	le	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	16	det	_	TokenRange=85:87
16	ville	ville	NOUN	_	Gender=Fem|Number=Sing	14	obj	_	SpaceAfter=No|TokenRange=88:93
17	.	.	PUNCT	_	_	14	punct	_	TokenRange=93:94

# sent_id = 2
# text = Ce n'était point de la troupe, mais des hordes débandées.
1	Ce	ce	PRON	_	Gender=Masc|Number=Sing|Person=3|PronType=Dem	7	nsubj	_	TokenRange=95:97
2	n'	ne	ADV	_	Polarity=Neg	7	advmod	_	SpaceAfter=No|TokenRange=98:100
3	était	être	AUX	_	Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin	7	cop	_	TokenRange=100:105
4	point	point	ADV	_	Polarity=Neg	7	advmod	_	TokenRange=106:111
5	de	de	ADP	_	_	7	case	_	TokenRange=112:114
6	la	le	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	7	det	_	TokenRange=115:117
7	troupe	troupe	NOUN	_	Gender=Fem|Number=Sing	0	root	_	SpaceAfter=No|TokenRange=118:124
8	,	,	PUNCT	_	_	12	punct	_	TokenRange=124:125
9	mais	mais	CCONJ	_	_	12	cc	_	TokenRange=126:130
10-11	des	_	_	_	_	_	_	_	TokenRange=131:134
10	de	de	ADP	_	_	12	case	_	_
11	les	le	DET	_	Definite=Def|Number=Plur|PronType=Art	12	det	_	_
12	hordes	horde	NOUN	_	Gender=Fem|Number=Plur	7	conj	_	TokenRange=135:141
13	débandées	débandé	VERB	_	Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part	12	acl	_	SpaceAfter=No|TokenRange=142:151
14	.	.	PUNCT	_	_	7	punct	_	TokenRange=151:152

# sent_id = 3
# text = Les hommes avaient la barbe longue et sale, des uniformes en guenilles, et ils avançaient d'une allure molle, sans drapeau, sans régiment.
1	Les	le	DET	_	Definite=Def|Number=Plur|PronType=Art	2	det	_	TokenRange=153:156
2	hommes	homme	NOUN	_	Gender=Masc|Number=Plur	3	nsubj	_	TokenRange=157:163
3	avaient	avoir	VERB	_	Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin	0	root	_	TokenRange=164:171
4	la	le	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	5	det	_	TokenRange=172:174
5	barbe	barbe	NOUN	_	Gender=Fem|Number=Sing	3	obj	_	TokenRange=175:180
6	longue	long	ADJ	_	Gender=Fem|Number=Sing	5	amod	_	TokenRange=181:187
7	et	et	CCONJ	_	_	8	cc	_	TokenRange=188:190
8	sale	sale	ADJ	_	Gender=Fem|Number=Sing	6	conj	_	SpaceAfter=No|TokenRange=191:195
9	,	,	PUNCT	_	_	12	punct	_	TokenRange=195:196
10-11	des	_	_	_	_	_	_	_	TokenRange=197:200
10	de	de	ADP	_	_	12	case	_	_
11	les	le	DET	_	Definite=Def|Number=Plur|PronType=Art	12	det	_	_
12	uniformes	uniforme	NOUN	_	Gender=Masc|Number=Plur	5	conj	_	TokenRange=201:210
13	en	en	ADP	_	_	14	case	_	TokenRange=211:213
14	guenilles	guenille	NOUN	_	Gender=Fem|Number=Plur	12	nmod	_	SpaceAfter=No|TokenRange=214:223
15	,	,	PUNCT	_	_	18	punct	_	TokenRange=223:224
16	et	et	CCONJ	_	_	18	cc	_	TokenRange=225:227
17	ils	il	PRON	_	Gender=Masc|Number=Plur|Person=3|PronType=Prs	18	nsubj	_	TokenRange=228:231
18	avançaient	avançer	VERB	_	Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin	3	conj	_	TokenRange=232:242
19	d'	de	ADP	_	_	21	case	_	SpaceAfter=No|TokenRange=243:245
20	une	un	DET	_	Definite=Ind|Gender=Fem|Number=Sing|PronType=Art	21	det	_	TokenRange=245:248
21	allure	allure	NOUN	_	Gender=Fem|Number=Sing	18	obl:arg	_	TokenRange=249:255
22	molle	mou	ADJ	_	Gender=Fem|Number=Sing	21	amod	_	SpaceAfter=No|TokenRange=256:261
23	,	,	PUNCT	_	_	25	punct	_	TokenRange=261:262
24	sans	sans	ADP	_	_	25	case	_	TokenRange=263:267
25	drapeau	drapeau	NOUN	_	Gender=Masc|Number=Sing	21	nmod	_	SpaceAfter=No|TokenRange=268:275
26	,	,	PUNCT	_	_	28	punct	_	TokenRange=275:276
27	sans	sans	ADP	_	_	28	case	_	TokenRange=277:281
28	régiment	régiment	NOUN	_	Gender=Masc|Number=Sing	25	conj	_	SpaceAfter=No|TokenRange=282:290
29	.	.	PUNCT	_	_	3	punct	_	TokenRange=290:291
</div>


<script type="text/javascript">
    Annodoc.activate(Config.bratCollData, Collections.listing);
</script>