import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "09"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
# _ = helper.fetch_data(DAY)
# _ = helper.fetch_test_data(DAY)

# read input
# puzzle_input = helper.read_lines_strip(DDATA_DAY)
# test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

# Ik wil weten op welke index de files staan... en met welke waarde
test_puzzle_input = ["2333133121414131402"]
puzzle_input = ["9953877292941648772616264775767428658883838268139271603033278826197512792138493841982683804757568110199215215571317977709849759733243569153182826948453096391192839170636590177283483639322341355356571986364617949975397540918247773979215998528235644578989248914549383222856258361161819260156064179996391961266912604423901066942216914217854276303630422886332436181925374685244140386687415960519939986071571752695323769824328476131628683469846953449356965554115590163216555863101814371821622059234754412952107359623159457288984076219639102672923788441086209687475033947873589869404644549648288825655198836028588849758065833038712860453278561629128194451431258781766519411112346859714318866328287132359827888716365493428476151089579915842478564939451742488886252065218125523183159190857623387862114038404875807456711075467031177026179750205411979310986675644388976287333467536853431970802022963588477642723084159186887657821874314618571866853797513937864514587980968044956444686467732298472170894497766918323313989886969526469633529546661027279823624833113451138628707972506178886396324927519720802441301629508356486017323180388623763989948880162984381152646523226343867258512950529356692920347519284216878459724924704970186844211512936492958969145515253550988722274195372951367390245879138326936518286787828968198545239675439493148123988429237919414017567595294484665559448842391210657615181447494553523776446532267054817592458089155662846972145085738154837254704780255233265839539332494366266516902612606710195278588341413778857094184455522295619322905549774623698189699719511648125899108615882115342478737810709114741866896212249015397547621569226132706216304760808527241479861767228540931024172157842126458576776380683512211257649443707337273380648643107092704128803048729763582791679854826974436392553365598596857637863553273786221684145827145730238920421773943241333959406553673780988853669665632969609245884147325675741263837125399283621726149153411123642513793771858546857241277844831758533096187329191192361899778775713766998925943964184060264161763929733129582060575776484674601481529293815518873595751299526753664798962691879371805960298650334921172837319162182739246199967977214958347582443988559040643576693613983710696599846618146310779935379427431572672232268710655256633119349722255254203244955318837479425818595058883159522172125123477046519623366023145950406420354021749856829987964757726770415929142616243825957194497512509467596299714567534620735696408398914927186575213628658975237577677626323098658718648480865153104585133043937441179934613447178932735183479837326461991514446224691285712816505421541188864390611231927199591053914773621381565619193490195121385563574974937319557723857518526440808767948253626897581294468744535957758397546675114268117396104199435561738635794559332173994456165773288285741399281892454219551981493991442413833474294486626217544268366367187026302572665585866062523091628551188032541345842830979462141866933637901250962086336185168431312716258429489520567518252710745963708049963539775895149137364332434462726826231991396378361974721851949847672075589859766537584973547169256840567516434560894380499411878764195355193035302887129050241641201250961293975638785637187254574782124164129680894281469996816781699791178788244086854725936594812845931719195684974841658662601927629977874565221515386218324555108186774423385493241557644638839648745875638947398840123565984453571979909757926026289488665321107437543533396842773526625812213616892173728395363984803489224172528070385657677840357753157114318886445125641565586266477412135619594119137841696238254810805831352342848580527035329868161013883669199278821722521150934216691484199172157412282530101185386123414891593078398445927193841635702990427485337758105257733624627347669857817741308281681138852620595044127944544789191465553956964159491666471443563074428589697914352241831984786723241080278698647317928130309765124361472562874661222045471149487043475720541326123514815943282820348967742558178412412414135353178865331357643149844765803666617637783611704835558719607962508717646147752059281064953822469035371530632815485687555634191623366675503964863051775824444147585169378779551097444690316481411899565016451780724170808454921319401678696177347666251347934156702386771942763348868028172776348376221253179521337346113247956732527952655817561927434210448881992966445210673859576794468665191678689247808451405275545236352187538233843619665694706337239238629011374993369793569671716258663085762456827453912170611066353248999297411819916182797156237051184841992592339435212385474955625835921165998283901542687939615294923238201528233713886046981860586775496659582487675458216668363267653677537891276083451310652735394592355427138739756320976992291532507217847550451795661114242814384594891669237013966088185015482234495358866928591321924652371181186059891815317081896037791581977716361599558822304391387735483664237887341241354720476735327889843575636129711374991549899215849997423991464614514032494340901368534549584243686387358667444626196855211095336941424745799841654930414637644887764944624460154358402017538730543447148671769981113256148070577868289940588936172424582914987473316044282311541518919665711224906238739936561817752250153374305931396036179219369821377252497568568250156341609471128816304032249564192531778921182065439631941065364089841617474463385572205840483077878490575839534354729862836339876229903613517085426363432773354826853553727541897789834211554825133921224365828334981123504958961594206053553483709481146157356685777532584438651184342081922416522783174781616231869739895864375446352560311667264286237668157023136176433614647667496539454023249784802548328650266339305842107410749492225394862298634745702428653812525763236232592227624283172694271450966649719068497169417549752646163911336765793418992437835021438772424649411248378669845923251194381342237048637531293784611443937070638020663256844440483533962245523972719859756097172238369373392295222475845599608442796664343615224131875268144890813116575168587370312823733117864491278973552882147562661155498388461856856096417976196946939215521019595764304737736732457555962679789795685091998488474875814627625782718444402428625496116555226690657446719238128945757654875735533343179170869860373430658018811866618327328349516792661612205669813710187113276357548366402212545322638361738991168755989667203647145273647810671530573735624845288764371816215665271159716953365444585027431379699640397396133954135399603516353538837439743725672776265038728578585314388042679131164764364916782745345891148730908727766796452872635667763119221265529827609971127211338743835439287769244138852763479488156867262982133086324759701067804283842637652643513062915552572674544126624195555859181218516745833792654984625525434969908913332568413561757349296827507576983591343669477240643151468133791480811118296898471163956771413336196924521689681975239548387366135114994140296399109120289440326062193917524311497525149644274261109920403890847086152399173383524712454978449751507711982653808947917370862492713527334423317470755494253968443310828711147875793790737777941979648735283670974310982185384938715444122943571584486790468686223050737945717443168060374439218990137794352738103172104081203540616278756022737823666377359476495058113531809154173651869062235699735456865283147317236961345364864143174825531969794223358613273988734337448524645190922460157534274138587463873091876911563198446067534862926368879149579728378627536920372452681275528637203370169322193447428262828442757385279978409260572137844773116733109354202018335753448549441752432917543886228918269131831685261378588686778745214467721133755350629892337532413155772155661770843849722217204041858875326692698269704389213544148426436910157511926252664598194994991788192828198815215037372649508323305617411625571476589324883275234479852239863295768848672139202532321314805070918588118513683239524512926965529976684378906482205985184060821781167395331492339731796769146936226821152019775539589339271720203722444456366866357468364573812310178513403124963434292151275573603722913575992914852883589445284177802981195971105110113989484531136494959365913526804010971849728042311681687314693218481080827850565234892063955349852588471318817254902334475443599637128319893352602739721472176798834599194920423044723085139290743820459840972279983531758188325052939078194377467836243858847092669467872285883926344384926274263937577177399950701461912024907550207629964475792654275021486682861910223495558515647369932527577572902056329292899547573522368723853583419243554985537561188981427342591621104257214911459025305414644567119630364513946941525928954067226375297896738117435356529266929343227541206047347590374175809725222431477072795446429553239519155655174341146322121899417517971189338325722094244277955154925413127213398053668087329787718430443643647722543351448418692647892257427147762060675321549823697741692958926170955567268863359256119845217578816568634365665049972646707321788928752035268251435352854173125659353951232052357042728319817854245221519498909755361373289455124657769436628483582995404124446441233779656713527941128284968664586924636639391774775280789095172267963614918279861057521725268142203380579175438751356214622911384075136631176385777283316056858534307613382838819856129169108992411130928925477748748530144320922327446234397645569292695277818484772194362724921844389784904760217759344449622660966950602823454091849232745637204591103669291960406660319452439420859249215337675363235879237826766884277864911393306360807324366543882373778648389361967739123729584616549178552744476746332754445395219710321429365523387961274560505030462515487167793773911538993530452526369493137329586884377438449964413176781512645532235714732731302256384676981998997151642750704650627994967097153921282175583794484461897143126483351614593925537722627048227440951741948327653712308520261755551553957530289983919144247464208578932488644685998949295738332096459074963769143737367715286187527799735481126019131839847446692599738953829510334861865667973788582160207271137999771170343921753530646441881022869740599798278145944297792836249928434329513953338922849683941634661182695935692196311042226291394274556493195172498035385417217735291460417343864399794432785160358335153076849061675616655490835826743224561268901283171560172088283696699934327628476277852140225420195138474031932785951669133014376160833370997377457726115737378723424595377237694221742519197860766568348541348833428897809124579373254093803035635829945642695656811936593457805186393857224962296759726898137115181533606758944354975496523996505235536766706193936323674340585472909881478514934473225911672147924622141079211041731216921235929892248454943966135775472866624750723998716271654119441915569854849591163924704783779792262648368686188548995264796952438896944723885089355784257269837256485911683691334317918123551995118977681349728828363883431614597743327057995124517859641461462356377288395241561213558438196457148862799319985340748954832959316820879776965657151475149375633084188412108723166617575745999369184320502934236512627493432826548953782837777277942780493745948184243148998399966953272085555080229080148146179725619923385073968396658296945578598332257666305551869799191538259737102618928973999981667265637627466825532682964989769865709231775914787778498132503727796091489164402118561155595993325563972767262765493980471717493210259351353529928629895535684620837697387512459930772657738265132643883989691393409743111518928267214289924758665415585392656130533629566186112736897496159352788173439368896277188975899742814112912813739528459834299081708482962353344772333378578692741081318029249139175548908776102924351689252743148831744650876264201744924868334864502987942236536565557895933767989377469672585372664944788137767856451024339660583641137989625271952559659267562877271041713882212583452759211557138510359355457890895387873165432781651072163088658470638362478994331540899444346424702557904589772079923338643555905298746940505036449965832594204047867880186843315085105487195767249374593516197171113677531376178317525457951850232521998936341652247294883847151367439469192990274524963838595196378995463184102730407272129282653173739551259929279566458579568451916453501893224037817599778827895273524489758495535789482246127035332932405983615225257762989690828331718684701684184125778065465372696911355159852151895936182087391454332221797364874172558149459565444770192824937412604482328869103630484639477543505731991768712121694934119011584219869350783182285761454465538818727790526933407273366396187349545066454647873943361281802598568883649385687042829966499329588215287773631495419633599476887056715930673619781030728414836910523113808879299936497475253339997684496262854826272970772819697177506448666177239614365360381350791865443816273273828583244622978865271719442538552722765457311134592736937457516736114548985056571744477435451157983552107955135463966989724232622628751779156153672892157240486288378960282572223048709686365918114526417711787596281665341526733774586240487410432339748683837245481659837781271485847159928071547912716218713142564523944036241628524684985255132632229990331751824331559981774410858912957662331752326912566441825151544340761894652485272380918117772495252342679734641416638837223741653674418399756570798991903997913519952464106672605527626430496387193383327879619522783347188635368911391227479528676442469435245213534688703719517419265051957185521748609029923389873348517678962796575076688046247625789820775791505289149760324194265683622654539469521835506065283591936846101591811099921898872820199185795335318551621835372792289789836671316093854510909017248712877873714851286883931236156384537925383360436132859033716588545054872487993611655915306040985611275276533519615193917531583341749853609624756175568081331741912297236360503568215792423932686023281452938140928794733890585319382758859567516985117051887525125499214770994885897412306645763921687363209773883190833817923775136220447014437011381510561222348831277153295883772138685762159863905019575986452261818830972399706088133422824547184164871445451067175294121896164293889424582334981070509685398313791861351214821891405925631066516417891995739529328642175988146433679510749627502070474880726321304222427719714961902511493234202170354816541253999573474570481228109694446414451382954212552685293745639446364275214787388115601487846636541766129894306219373023834342249335191233831144582655661128523374495992114042805681178698213357586210913259144258601479509017174184307089298281567450622989522471945693646038105114432888879393537247714269348637946358586958899778598773856996917888237995202344466916259996678574364575816899941324625212348696579931572280604345981974941844709488559775366454922696285386801793781112635051736437196851189552633886155457361028185159453475523640942448543459676996421172802111845375474212684082732732933461257944945073599841559516299858462394515688181879665518203131111776218186277233568961686098214484676830387537411364645622166556122851775091246399955185619791636473198797237252279753184933369173477516203735929740256590997320662680852980819684834918541817577678984493402048714915593674615223509178748196418953997351419225563271328654369980186463599542569735524071462652189446131070186215319695804577596442688495611455332884405489489390185736868266647763407380821864274485608860565942434434423993389664321047225233137460665253672182679983393727189921878353743652129234947096141311239321806082291019628359543928493543341449679860852984311682683033222160211386565374719359471486482263945654895096999450905890626723789190553023834242654662703756197650993790102031524390231820594075412174918728431776959982686012221851925164748366541987664360669767285313328080269498171069777567929655123120974939533312585824953325566942739742409382525885782137879263116712445562746784591424479220418234327760581298196325201058206456456161843659871476859283668417909839669290288799931946149578364937793217954162273310912256718878624997376929504992892228117854135466132748247468847342744217523258667588255982204997924163607999543980521780756883293666675523674128128370722495386418536353994947103520412942841923337425975419479679573737585993557126919739174181584626496512223086892050984165442933251460234261336248376049559234933656709219479055247942971823158066399672116785943691707266193574637985393752333758304132163559861637508396289321157716618783802916582120477368554013603098793261556637601356607819254818648759792998566868842773792694828174738980977493318979124945593124814550678718994787239623198340872959785630591938973714485233417651461597488198383845996789948733925916132580201418466988814029397084186792314269357150146959749010768587751275866231869564381996322522153452515483829980649580552936939572834486684831703735918449905053371313731328873738997414197332754185655051202030472452807961891922271616882273368314553722197428675422885357442669991316178620695449629088115655122870826914388013269024862841994011931620224371963948908348171534975611517517472854964618684227328311312332623079203568393877644124858919946279903788635293904493405191284628862879799743708169799313569427538175624482144075273685104954745945751192457421159326711469203948971118311742301064458292115224416132269152118844129443263425526331118433398264149280848622411194544913822248199151374490277618385614613776383821781280571848446177145537943192652181583364308498334157415622344461626481354866954542328447772810328745557865553411344057855593359045751762174015212152659130232055949368817119541635571469499825935419881870578118275694211463268227213628488357528091959315762163747313325074492247267214102899887846503594623335923880241579858734241541595635886586723679156020472412148312207233327190361633502299131621856444314027529439351516366881357367595155528782338778808919312730274375424094713484594940938516456911545494121859478940207291696012892792799025467956777812544748588216436321444076611987424715711629372570701579883728133890193725947329244964881392922827239921178095929880923292566367803342911883167815209987846966509486619693579911134198652885904333122261887952153075363267558853542731643288211699512199709320759356336111788135551786444417803039769821625234447446598018888026451663714253327064105330236948535030542896901235831977428370292747877756375823534595935922377339369110838966477483468958903826246650209843278950702998377830313517389743602971541210801871265523295019715541192070185272711477523053444026492532302870847090234918557428976063811642983043184591836755893995244320464588943510677375646074418446313151749040933259973365329573823598244359867317381375534718289686458870178218881545803499331770763874414816976920338913812974753988387820916866729537198877822274703321463443746114173173225572217166828942368644314265807761275966639477249353581066104354879242589517199243313675497778353914791790938347638374483324171264212738101631992098344615439078792378397114135187318336878285312923574875995811106887637468649641412441579594648937956133348367699970134775621765354772399570764034559745149116141963467585186676118599313161153029725127722895562733267097895450155025124834417961294842519720664070331151793630236246708734634312945815178290833885442815338795499348803493878042382150262149959934641010191882558744137666944794483730719045906956757666911684386728313714437312628942255599764631615742877463388952916563801236249973924451767615898111417019918693593727185221115347312524188597946681239674666511571035161443246671276897119986573457236856577127418443929435179927733320163426341733736679833298763529855287894395377028279496435430158914522676601751669746655389773828539815296783161247729789828580983759647854855034492976721720176672974814191665968377679057111757554567632341809178939763698516466521754449277681728248314745265416923943105833124832186658567050623356888616753862411790965125587883649825467173538445845222588678831547771055609250801044119039714391542276714523732863532885628165471526409163824"]
chosen_puzzle = test_puzzle_input
chosen_puzzle = list(chosen_puzzle[0])

# chosen_puzzle = "919090909"
file_blocks = [int(x) for x in chosen_puzzle[::2]]
free_space = [int(x) for x in chosen_puzzle[1::2]]

index_free_space = []
n = len(free_space)
for i in range(n):
    file_block = file_blocks[i]
    if len(index_free_space):
        last_pos = index_free_space[-1] + 1
    else:
        last_pos = 0

    for j in range(free_space[i]):
        new_pos = file_block + last_pos + j
        index_free_space.append(new_pos)

import itertools
file_blocks_derp = list(itertools.chain(*[size * [ID] for ID, size in enumerate(file_blocks)]))


for i_loc in index_free_space:
    x = file_blocks_derp.pop()
    file_blocks_derp.insert(i_loc, x)

print(file_blocks_derp)
print(sum([int(x) * i for i, x in enumerate(file_blocks_derp)]))

# calculate score...
# 6104973916432 -- too low
# wat doet een nul...?
# hmm nee die zit wel al in de test case...