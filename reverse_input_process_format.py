import os
import re
import numpy as np
import pandas as pd
import ujson as json
import csv

#plan
"""
Reads line
Strip edge bracket
Split at "]"
	[...data , [...data
Strip at "["
	#...data, ...data
Split at ,
Perform reverse scaling on 35 attributes
[[0.1703552007675171, 0.008318169042468071, 0.014850514009594917, -0.15467634797096252, -0.034450970590114594, -0.04534415528178215, -0.11420778185129166, -0.10802504420280457, 0.08319272845983505, 0.013963010162115097, -0.10405183583498001, 0.0010441653430461884, -0.05286278575658798, -0.1830180138349533, 0.04678261652588844, 0.11530353873968124, -0.1266646683216095, 0.13977745175361633, -0.09441554546356201, -0.06027105078101158, 0.08910198509693146, -0.06863599270582199, -0.12658973038196564, 0.3874613344669342, 0.10431525111198425, 0.05705057829618454, -0.06168666109442711, 0.2177785187959671, 0.09919168055057526, 0.10060480237007141, -0.16567766666412354, 0.15393288433551788, 0.06897489726543427, -0.15328410267829895, -0.10735123604536057], [0.20551753044128418, 0.020637819543480873, 0.020994218066334724, -0.1626526415348053, -0.009381473064422607, -0.054685331881046295, -0.11236138641834259, -0.10604862868785858, 0.08647587150335312, 0.002249165903776884, -0.11657624691724777, 0.013307631947100163, -0.05450589954853058, -0.2060597836971283, 0.03893290460109711, 0.1301097273826599, -0.14707691967487335, 0.1449890285730362, -0.10189568996429443, -0.05277132987976074, 0.142201229929924, -0.08780910819768906, -0.14097796380519867, 0.40974724292755127, 0.11093433946371078, 0.0822160542011261, -0.05329813063144684, 0.2616669237613678, 0.10134731978178024, 0.10005342960357666, -0.17587731778621674, 0.1630152314901352, 0.07828107476234436, -0.18480932712554932, -0.09579943120479584], [0.24294981360435486, 0.028685199096798897, 0.02416219562292099, -0.17470553517341614, 0.019063353538513184, -0.06601621210575104, -0.11060050129890442, -0.10832282155752182, 0.08485113829374313, -0.011875242926180363, -0.12823045253753662, 0.024835046380758286, -0.054004136472940445, -0.2271200716495514, 0.033651672303676605, 0.14885929226875305, -0.16098925471305847, 0.15656034648418427, -0.10804511606693268, -0.04705405980348587, 0.2140910029411316, -0.10427393764257431, -0.15992923080921173, 0.4319896101951599, 0.11783725768327713, 0.11066091060638428, -0.048075854778289795, 0.3077205717563629, 0.10859610140323639, 0.1010315790772438, -0.18981309235095978, 0.17159989476203918, 0.09960000962018967, -0.2167222499847412, -0.0873759463429451], [0.28798285126686096, 0.03062424063682556, 0.022742407396435738, -0.1902712881565094, 0.05383351445198059, -0.07593325525522232, -0.11222660541534424, -0.11003927886486053, 0.07914010435342789, -0.030940094962716103, -0.14056181907653809, 0.039356134831905365, -0.054344113916158676, -0.24562114477157593, 0.026833290234208107, 0.17039482295513153, -0.17026887834072113, 0.1714785397052765, -0.11622337996959686, -0.04590494558215141, 0.3028298318386078, -0.12225741893053055, -0.1864788830280304, 0.4507427215576172, 0.12463509291410446, 0.14286690950393677, -0.04313569888472557, 0.3572987914085388, 0.12235376238822937, 0.10219420492649078, -0.208017498254776, 0.18115973472595215, 0.13585448265075684, -0.2534966468811035, -0.08078767359256744], [0.36998558044433594, 0.01843869313597679, 0.015564262866973877, -0.20429889857769012, 0.1102600246667862, -0.07846720516681671, -0.11255044490098953, -0.12636195123195648, 0.06473439931869507, -0.04551219195127487, -0.15391410887241364, 0.06069023162126541, -0.05584187060594559, -0.262689471244812, 0.016865471377968788, 0.20401915907859802, -0.175654798746109, 0.2017369568347931, -0.1262291669845581, -0.045849889516830444, 0.44397974014282227, -0.1341395378112793, -0.21948596835136414, 0.4396626949310303, 0.14206258952617645, 0.1848742812871933, -0.024313461035490036, 0.4300088584423065, 0.1294901967048645, 0.12675116956233978, -0.23883378505706787, 0.22688280045986176, 0.18970264494419098, -0.30991148948669434, -0.07797828316688538], [0.880490243434906, -0.2654988467693329, 0.0771368145942688, 0.11787440627813339, 0.3035739064216614, 0.0417884886264801, -0.011811737902462482, -0.1500421017408371, 0.19632279872894287, 0.0037652775645256042, -0.094241201877594, 0.08298491686582565, 0.5295597314834595, -0.17874985933303833, 0.40082722902297974, 0.2586804926395416, -0.5398615598678589, 0.9714838266372681, -0.07507283985614777, -0.016704272478818893, 1.9973669052124023, -0.12413965910673141, -0.06974992156028748, 0.5424372553825378, 0.651886522769928, 0.4481115937232971, 0.3640686273574829, 0.9731572270393372, -0.03076799213886261, 0.16804704070091248, -0.19516301155090332, 3.4214587211608887, 0.13758283853530884, -0.4225139915943146, 0.01410047709941864], [0.26578500866889954, 0.5214635133743286, 0.3722369968891144, -0.20484629273414612, 0.4845183491706848, -0.3460542559623718, -0.21835660934448242, -0.15548478066921234, 0.1066795065999031, -0.0746510922908783, 0.33292534947395325, 0.005371473729610443, 0.1690869927406311, -0.18270504474639893, -0.21250317990779877, 0.2126469761133194, -0.829482913017273, 0.2454182505607605, -0.7766472101211548, 1.5408790111541748, 0.8595933318138123, -0.1940971463918686, -0.6169726848602295, 0.9053964614868164, 0.14806538820266724, 0.2034006416797638, 0.01601911336183548, 0.2339002788066864, 0.164165198802948, 0.11436544358730316, 0.9664990305900574, 0.022752828896045685, 0.2404673844575882, -0.43082424998283386, -0.19450251758098602], [0.11210869997739792, 0.5214635133743286, -0.022741148248314857, 0.08394033461809158, 0.3450753092765808, -0.3281552791595459, 0.0520075224339962, -0.18504653871059418, 0.19980865716934204, -0.11268451064825058, -0.1828957498073578, 0.03598679602146149, 0.034167319536209106, -0.33325159549713135, 0.10255840420722961, 0.36022764444351196, -0.328961580991745, 2.060582160949707, -0.0810193419456482, -0.19835448265075684, 0.5224752426147461, -0.11405760049819946, -0.30426645278930664, 0.7494516968727112, 0.2767355442047119, 0.17368799448013306, 0.07978381216526031, 0.11069078743457794, 0.03150900453329086, -0.08241422474384308, -0.3073997497558594, 0.9603269100189209, 0.27527618408203125, -0.4653369188308716, 0.06964953988790512], [0.49629947543144226, 0.2966171205043793, -0.013593405485153198, -0.0234987735748291, 0.36818280816078186, -0.3308006525039673, -0.042529426515102386, -0.2083614468574524, 0.17752037942409515, -0.14577192068099976, -0.2289780080318451, 0.0005964748561382294, 0.06094568222761154, -0.368072509765625, 0.09612569212913513, 0.34349799156188965, -0.35360652208328247, 1.6975494623184204, -0.08204486966133118, -0.12969380617141724, 0.9017331004142761, -0.11729533970355988, -0.3037727177143097, 0.9053964614868164, 0.24261052906513214, 0.23376032710075378, 0.10372328758239746, 0.4803192615509033, 0.10890809446573257, -0.0010133497416973114, -0.27611589431762695, 0.7845317721366882, 0.29854851961135864, -0.43686121702194214, 0.12924274802207947], [0.573137640953064, 0.40904033184051514, 0.0070015136152505875, -0.2518925666809082, 0.3929596245288849, -0.32246363162994385, -0.0019829757511615753, -0.16361519694328308, 0.09481510519981384, -0.12070286273956299, -0.33102864027023315, -0.034187350422143936, 0.40139469504356384, -0.36148399114608765, 0.024899594485759735, 0.32512253522872925, -0.3278665244579315, 0.7313538789749146, -0.24583928287029266, -0.05216507241129875, 1.4495500326156616, -0.16958004236221313, -0.277732253074646, 0.9053964614868164, 0.1875602900981903, 0.31660473346710205, -0.031433794647455215, 0.6651334762573242, 0.05213058739900589, 0.11737751215696335, -0.35120177268981934, 0.1398482769727707, 0.33090996742248535, -0.39860913157463074, 0.04530433192849159], [0.9573283791542053, -0.04065246134996414, -0.009743895381689072, -0.03773101419210434, 0.4550224542617798, -0.3376144766807556, -0.1195465475320816, -0.19934207201004028, 0.17447282373905182, -0.13857197761535645, -0.2649500072002411, -0.04877075180411339, 0.06413529068231583, -0.40132176876068115, 0.11444483697414398, 0.40963494777679443, -0.3629818558692932, 2.242098569869995, -0.12507186830043793, -0.06296117603778839, 1.618109107017517, -0.14560207724571228, -0.41891443729400635, 0.9053964614868164, 0.36500445008277893, 0.4438437521457672, 0.0637868270277977, 0.9115524888038635, 0.18063847720623016, -0.03527887165546417, -0.28585147857666016, 0.11763463914394379, 0.4527120292186737, -0.45660626888275146, 0.40708863735198975], [0.9573283791542053, 0.07177073508501053, 0.008527431637048721, -0.06905589252710342, 0.5192382335662842, -0.3527618646621704, -0.1595853567123413, -0.2304483950138092, 0.19635792076587677, -0.1308308243751526, -0.2379390299320221, -0.08750128746032715, 0.017178930342197418, -0.3827023208141327, 0.07798315584659576, 0.40308016538619995, -0.3510943055152893, 2.242098569869995, -0.12077964842319489, -0.07357698678970337, 1.5759693384170532, -0.17500633001327515, -0.45786577463150024, 0.9053964614868164, 0.3629930019378662, 0.4860629737377167, 0.06356371194124222, 0.9115524888038635, 0.21209606528282166, -0.04940667003393173, -0.28297901153564453, 0.022752828896045685, 0.5317789316177368, -0.428555965423584, 0.371616005897522], [1.187842845916748, 0.07177073508501053, 0.03736858814954758, -0.10204891860485077, 0.5621732473373413, -0.30123260617256165, -0.052869442850351334, -0.2279483675956726, 0.20321893692016602, -0.07508283108472824, -0.23309370875358582, -0.06948348134756088, 0.14506462216377258, -0.40725386142730713, 0.12009628117084503, 0.37692350149154663, -0.4113197326660156, 1.5160330533981323, -0.16745293140411377, -0.04521617293357849, 1.0660412311553955, -0.15396572649478912, -0.39643359184265137, 0.9053964614868164, 0.3068240284919739, 0.42075014114379883, 0.018077082931995392, 1.0174434185028076, 0.19943398237228394, -0.027575276792049408, -0.2446700483560562, 0.7259333729743958, 0.5535284280776978, -0.3833649754524231, 0.12603001296520233], [0.573137640953064, 0.24040552973747253, -0.010596245527267456, -0.07387620955705643, 0.5488451719284058, -0.39466118812561035, -0.07313123345375061, -0.2340863049030304, 0.16611485183238983, -0.14739173650741577, -0.23970931768417358, -0.10597778856754303, -0.0028848685324192047, -0.4103391766548157, 0.037577494978904724, 0.4433080554008484, -0.25032415986061096, 2.6051313877105713, -0.1306988149881363, -0.14076729118824005, 1.2809909582138062, -0.1595490276813507, -0.5049048066139221, 0.9053964614868164, 0.2421678602695465, 0.4705612361431122, -0.043374739587306976, 0.6035287380218506, 0.22900131344795227, -0.10837597399950027, -0.2766839563846588, -0.32883745431900024, 0.6258013248443604, -0.41840893030166626, 0.35721299052238464], [1.7257099151611328, 0.19597391784191132, 0.10179335623979568, -0.0575798898935318, 0.6555019021034241, -0.23750145733356476, -0.211948424577713, -0.19335785508155823, 0.2132415622472763, -0.08983507007360458, -0.2014836072921753, -0.08909562975168228, 0.029197372496128082, -0.3579529821872711, 0.08533591777086258, 0.3560669422149658, -0.47947949171066284, 1.1530002355575562, -0.15869078040122986, 0.09695235639810562, 1.5759693384170532, -0.1726701557636261, -0.33089679479599, 0.9053964614868164, 0.4417954385280609, 0.6432370543479919, 0.2228274941444397, 1.5275999307632446, 0.2770123779773712, 0.06473323702812195, -0.20837652683258057, 0.9310277104377747, 0.5890256762504578, -0.4303429126739502, 0.16945700347423553], [0.573137640953064, 0.5776751041412354, 0.09270258247852325, -0.0375809371471405, 0.5506682991981506, -0.3735309839248657, 0.025547903031110764, -0.2133646309375763, 0.2069655954837799, -0.0640064999461174, -0.22788774967193604, -0.04577255994081497, -0.004711683839559555, -0.3569168448448181, 0.013432413339614868, 0.4454135596752167, -0.2748309075832367, 2.423614978790283, -0.21840554475784302, -0.058836888521909714, 1.5759693384170532, -0.19008955359458923, -0.46040022373199463, 0.7963219881057739, 0.3404701054096222, 0.5924360752105713, 0.07253426313400269, 0.6035287380218506, 0.14304029941558838, -0.09574510157108307, -0.23541401326656342, 0.16483855247497559, 0.6206427812576294, -0.4870304763317108, 0.2601076662540436], [0.880490243434906, 0.12798233330249786, 0.08040639758110046, -0.16566216945648193, 0.5978419780731201, -0.2064945101737976, 0.03258891776204109, -0.1779521107673645, 0.23070098459720612, 0.006933814845979214, -0.26213154196739197, -0.04889417067170143, 0.33731216192245483, -0.3039797246456146, 0.12829244136810303, 0.360900342464447, -0.3589934706687927, 0.8786789774894714, -0.18784482777118683, 0.00045943446457386017, 1.32313072681427, -0.22266729176044464, -0.3255489766597748, 0.9053964614868164, 0.19070032238960266, 0.610077977180481, 0.06204479932785034, 0.8499477505683899, 0.026658210903406143, 0.06583419442176819, -0.22292691469192505, 1.5170115232467651, 0.5668515563011169, -0.375602662563324, 0.01030922681093216], [0.8036521077156067, 0.07177073508501053, 0.10316114127635956, -0.08084350824356079, 0.5166423320770264, -0.3246309161186218, -0.03151272237300873, -0.20609043538570404, 0.21908627450466156, -0.0488366037607193, -0.26516199111938477, -0.0247800350189209, 0.003301559016108513, -0.381538450717926, 0.04917217791080475, 0.4517432451248169, -0.2697297930717468, 2.242098569869995, -0.1808914691209793, -0.01088021695613861, 1.660248875617981, -0.2071630358695984, -0.46096035838127136, 0.8452790975570679, 0.30404427647590637, 0.6280771493911743, 0.060695670545101166, 0.8499477505683899, 0.17205467820167542, -0.060748662799596786, -0.19086423516273499, 0.13228844106197357, 0.652942955493927, -0.43767136335372925, 0.33683282136917114], [1.187842845916748, 0.4652519226074219, 0.20610570907592773, -0.27628451585769653, 0.5812023878097534, -0.2171684056520462, -0.14266309142112732, -0.14177802205085754, 0.21902665495872498, 0.049237560480833054, -0.3318462669849396, -0.04102514684200287, -0.025722209364175797, -0.29280364513397217, -0.09277407079935074, 0.29729992151260376, -0.3716351389884949, -0.11761455237865448, -0.26886165142059326, 0.12991419434547424, 1.9130873680114746, -0.2839668393135071, -0.2701164782047272, 0.8532090187072754, 0.26633137464523315, 0.6990199089050293, 0.15354779362678528, 1.2195762395858765, 0.15702953934669495, 0.13262821733951569, -0.22934626042842865, 0.7845317721366882, 0.6112480163574219, -0.39030444622039795, -0.07406657934188843], [1.0341665744781494, -0.09686405956745148, 0.17655137181282043, -0.4065994620323181, 0.5343137383460999, -0.15880772471427917, -0.1384042501449585, -0.10915905237197876, 0.1468437910079956, 0.07842637598514557, -0.34716522693634033, -0.1024823933839798, 0.009070304222404957, -0.31624680757522583, -0.08021276444196701, 0.31892234086990356, -0.3226984441280365, -0.6621637344360352, -0.2552375793457031, 0.09447284787893295, 1.786668062210083, -0.273532509803772, -0.3046974837779999, 0.8276867866516113, 0.04556960240006447, 0.652031660079956, -0.10212595015764236, 0.9731572270393372, 0.13591735064983368, 0.20876701176166534, -0.2238519787788391, 0.09624773263931274, 0.6439089179039001, -0.3920101523399353, -0.029653236269950867], [1.2646809816360474, -0.15307565033435822, 0.15454870462417603, -0.3697096109390259, 0.5939161777496338, -0.13488627970218658, -0.11624407768249512, -0.09167729318141937, 0.13968922197818756, 0.11394109576940536, -0.3011193871498108, -0.09302937984466553, 0.2091471403837204, -0.2992756962776184, 0.013536687940359116, 0.3228617310523987, -0.32337692379951477, -0.29913094639778137, -0.22715002298355103, 0.11685704439878464, 1.786668062210083, -0.2633981704711914, -0.31473439931869507, 0.9053964614868164, 0.11317623406648636, 0.6889404058456421, -0.09936989843845367, 1.1579715013504028, 0.12404407560825348, 0.2053428590297699, -0.22173769772052765, 0.11089804023504257, 0.6787834763526917, -0.33976981043815613, 0.009762324392795563], [0.880490243434906, -0.15307565033435822, 0.1603783369064331, -0.19537794589996338, 0.6065725088119507, -0.16782039403915405, 0.006693120114505291, -0.17286455631256104, 0.2266348898410797, 0.10007824003696442, -0.30519479513168335, -0.040490373969078064, 0.01573195494711399, -0.34457191824913025, 0.02374071627855301, 0.3925134241580963, -0.2682720124721527, 0.9714838266372681, -0.19076043367385864, 0.02690126746892929, 1.1815807819366455, -0.24085702002048492, -0.4283445477485657, 0.7621111869812012, 0.12201087176799774, 0.666827917098999, -0.13917645812034607, 1.0347620248794556, 0.18877172470092773, 0.03316774219274521, -0.1812737137079239, 0.13227736949920654, 0.7388133406639099, -0.4037023186683655, 0.14703676104545593], [0.9573283791542053, -0.20928725600242615, 0.12291546911001205, -0.25736933946609497, 0.6306476593017578, -0.1257007122039795, -0.10606469213962555, -0.13918285071849823, 0.15729647874832153, 0.10259624570608139, -0.2867879569530487, -0.05539252609014511, -0.009274967014789581, -0.3450913429260254, 0.01388712041079998, 0.36600548028945923, -0.2975027561187744, 0.6084510684013367, -0.17941874265670776, 0.014622749760746956, 1.32313072681427, -0.24827542901039124, -0.4196000099182129, 0.9053964614868164, 0.05300468951463699, 0.7030922174453735, -0.12298627197742462, 0.9115524888038635, 0.17733174562454224, 0.10951697081327438, -0.19793500006198883, 0.13267824053764343, 0.7433890700340271, -0.36378395557403564, 0.10206985473632812], [1.8025480508804321, -0.03475112468004227, 0.21228452026844025, -0.32302162051200867, 0.7217423915863037, -0.10476107895374298, -0.2662665843963623, -0.12131732702255249, 0.14586570858955383, 0.13568517565727234, -0.27175742387771606, -0.0958850234746933, -0.009810835123062134, -0.3176976442337036, -0.04025726020336151, 0.3692933917045593, -0.3905407190322876, -0.29913094639778137, -0.25209373235702515, 0.12305304408073425, 1.8709475994110107, -0.2937496304512024, -0.3387336730957031, 0.759535551071167, 0.21409806609153748, 0.788223922252655, 0.026863668113946915, 1.3595011234283447, 0.2825414836406708, 0.21887367963790894, -0.18276488780975342, 0.16083937883377075, 0.8026900291442871, -0.3842509388923645, -0.016227051615715027], [2.955120325088501, 0.2966171205043793, 0.3259802758693695, -0.05384650453925133, 0.9337878227233887, -0.011928347870707512, -0.24451813101768494, -0.14726173877716064, 0.39479804039001465, 0.16257323324680328, -0.13898113369941711, -0.03477775678038597, -0.2394305020570755, -0.2834617793560028, 0.17381170392036438, 0.27912649512290955, -0.6109535694122314, 0.46366408467292786, -0.16323858499526978, 0.24980220198631287, 1.9130873680114746, -0.25128069519996643, -0.2728009819984436, 0.9053964614868164, 0.6112171411514282, 0.9768977165222168, 0.4024830162525177, 2.2668569087982178, 0.23884396255016327, 0.17643146216869354, -0.1967822015285492, 1.6635074615478516, 0.7994898557662964, -0.3921881914138794, -0.06451468914747238], [1.1692692041397095, -0.09686405956745148, 0.22771486639976501, 0.03261084109544754, 0.7345938682556152, -0.23806971311569214, 0.0066826604306697845, -0.2077869325876236, 0.29752328991889954, 0.03517784923315048, -0.1873781532049179, -0.04438254237174988, 0.07154050469398499, -0.4041050672531128, 0.08186989277601242, 0.4673331379890442, -0.3463612198829651, 2.423614978790283, -0.0535811223089695, -0.020232845097780228, 0.5224752426147461, -0.21619661152362823, -0.5105589628219604, 0.7857042551040649, 0.26338711380958557, 0.6549887657165527, -0.10280182957649231, 0.9731572270393372, 0.2569766640663147, -0.049557216465473175, -0.05974942445755005, 0.23965495824813843, 0.7977827787399292, -0.5094025135040283, 0.28882795572280884], [0.7268139123916626, 0.352828711271286, 0.14355072379112244, -0.2525934875011444, 0.6285463571548462, -0.22468623518943787, -0.007693275809288025, -0.15653085708618164, 0.1737481653690338, 0.04715108126401901, -0.24644875526428223, -0.07084555178880692, 0.044783636927604675, -0.32880786061286926, -0.004786375910043716, 0.33248811960220337, -0.326529860496521, 0.6084510684013367, -0.20091360807418823, 0.040476180613040924, 1.4074102640151978, -0.25108110904693604, -0.39342477917671204, 0.9053964614868164, 0.09682823717594147, 0.6599997878074646, -0.06590917706489563, 0.8499477505683899, 0.1818227469921112, 0.11139571666717529, -0.22698217630386353, 0.2074548900127411, 0.6627267599105835, -0.40302443504333496, -0.0066982451826334], [0.34262317419052124, -0.06845373660326004, 0.11431332677602768, -0.22176966071128845, 0.6107866764068604, -0.2257697880268097, -0.00636628270149231, -0.18261903524398804, 0.17872700095176697, 0.009265538305044174, -0.249069482088089, -0.05479452759027481, 0.021279439330101013, -0.36144137382507324, 0.028098009526729584, 0.40948331356048584, -0.26975274085998535, 1.1530002355575562, -0.18582046031951904, -0.03702465817332268, 1.3652704954147339, -0.22189313173294067, -0.46525928378105164, 0.7886053323745728, 0.009672516956925392, 0.6848900318145752, -0.12946325540542603, 0.6035287380218506, 0.15359392762184143, 0.038803618401288986, -0.19525842368602753, 0.22513476014137268, 0.72868812084198, -0.4434705972671509, 0.14100228250026703], [1.1275668144226074, -0.20928725600242615, 0.15473110973834991, -0.13316532969474792, 0.6184394359588623, -0.19744957983493805, -0.07800287008285522, -0.22869384288787842, 0.22686010599136353, -0.03348381072282791, -0.2508218288421631, 0.016807936131954193, 0.08098209649324417, -0.3914569020271301, 0.16649946570396423, 0.4383352994918823, -0.24239256978034973, 2.242098569869995, -0.11279302835464478, 0.0004750434309244156, 1.3652704954147339, -0.1978558599948883, -0.5245344042778015, 0.9053964614868164, 0.20686514675617218, 0.772209644317627, -0.02360530197620392, 1.0347620248794556, 0.21722936630249023, -0.029666777700185776, -0.1280709207057953, 0.26730579137802124, 0.8186783194541931, -0.39671823382377625, 0.3099307119846344], [1.2646809816360474, -0.09242352843284607, 0.1836434006690979, -0.1967546045780182, 0.6691979169845581, -0.16676926612854004, -0.14810356497764587, -0.19621196389198303, 0.2189486026763916, 0.008550215512514114, -0.25222280621528625, -0.0343150869011879, -0.025964422151446342, -0.34693634510040283, 0.040611766278743744, 0.3901660144329071, -0.3411743640899658, 1.1530002355575562, -0.20964330434799194, 0.09381186962127686, 1.9552271366119385, -0.2331467568874359, -0.45164400339126587, 0.760846734046936, 0.2737356722354889, 0.8407849669456482, 0.04620268940925598, 1.28118097782135, 0.25427913665771484, 0.08647109568119049, -0.14159463346004486, 0.2603040337562561, 0.793660044670105, -0.40969228744506836, 0.2245841920375824], [1.4951955080032349, 0.07177073508501053, 0.2875717282295227, 0.04952606186270714, 0.7883340120315552, -0.0810069888830185, -0.029441725462675095, -0.2030162811279297, 0.38491755723953247, 0.09702736884355545, -0.1749643087387085, 0.036106906831264496, -0.008967608213424683, -0.2409096509218216, 0.2519422173500061, 0.3778601586818695, -0.5690085887908936, 1.5160330533981323, -0.1270519196987152, 0.15873518586158752, 2.2502055168151855, -0.20217815041542053, -0.34934985637664795, 0.781953752040863, 0.5516030788421631, 1.0049140453338623, 0.4765775799751282, 1.5892046689987183, 0.11571608483791351, 0.0581463947892189, -0.15623173117637634, 2.835474967956543, 0.7299814820289612, -0.4768417179584503, 0.10889361798763275], [0.573137640953064, -0.3217104375362396, 0.16654948890209198, -0.15024572610855103, 0.5835888981819153, -0.2041882425546646, 0.05631359666585922, -0.19300326704978943, 0.25620532035827637, 0.05834707245230675, -0.22476071119308472, 0.0033062174916267395, 0.047133609652519226, -0.3713235855102539, 0.07590343058109283, 0.4217657148838043, -0.30576401948928833, 1.3345166444778442, -0.10372476279735565, -0.05368839576840401, 0.2696366608142853, -0.1867595911026001, -0.4837968051433563, 0.7567334175109863, -0.037741806358098984, 0.6070985198020935, -0.19134923815727234, 0.4803192615509033, 0.13319481909275055, 0.008156023919582367, -0.10198171436786652, 0.27481675148010254, 0.7493230700492859, -0.4122679531574249, 0.1177578866481781], [1.0341665744781494, -0.3217104375362396, 0.20742635428905487, -0.26132112741470337, 0.5856114625930786, -0.13818702101707458, -0.07240165770053864, -0.16449517011642456, 0.17864209413528442, 0.06051797792315483, -0.25071704387664795, -0.026180358603596687, 0.04658733308315277, -0.3636195659637451, 0.05545233190059662, 0.36609315872192383, -0.34385788440704346, 0.4269346296787262, -0.18087375164031982, 0.05197633057832718, 1.1124318838119507, -0.20872069895267487, -0.4013461172580719, 0.7355109453201294, 0.08144892752170563, 0.6935186386108398, -0.08699080348014832, 1.0255911350250244, 0.23903296887874603, 0.14322279393672943, -0.11496572196483612, 0.26342880725860596, 0.7384066581726074, -0.40229904651641846, 0.048290204256772995], [0.9573283791542053, -0.14929792284965515, -0.20628869533538818, -0.19656848907470703, 0.752743661403656, -0.2331680804491043, -0.5451942086219788, -0.2114425003528595, 0.4236917495727539, 0.05493505671620369, -0.33253365755081177, 0.02594456449151039, -0.04042023420333862, -0.29563772678375244, 0.011501587927341461, 0.6119992733001709, -0.28263965249061584, 1.5160330533981323, -0.06575539708137512, 1.4809037446975708, 1.4074102640151978, -0.2737021744251251, -0.6169726848602295, 0.7100008726119995, 0.0682438313961029, 0.7537798881530762, 0.02250361442565918, 0.9115524888038635, 0.19223985075950623, 0.12929674983024597, 0.6848337650299072, 0.27458247542381287, 0.7940025329589844, -0.43082424998283386, 0.03141660615801811], [1.0341665744781494, -0.546556830406189, 0.1499943733215332, -0.14496158063411713, 0.6968557834625244, -0.10231241583824158, -0.13427704572677612, -0.15636298060417175, 0.2482113391160965, 0.09426580369472504, -0.20474253594875336, -0.03897197172045708, -0.04926607012748718, -0.38245633244514465, 0.11561715602874756, 0.43013796210289, -0.31079530715942383, 0.9714838266372681, -0.10554669797420502, -0.034002870321273804, 1.32313072681427, -0.23373517394065857, -0.47125691175460815, 0.9053964614868164, 0.12466572225093842, 0.7462367415428162, -0.1032373234629631, 0.9731572270393372, 0.1086965948343277, 0.1103542223572731, -0.13027149438858032, 0.32642316818237305, 0.8198232054710388, -0.3348711431026459, 0.1355803906917572], [1.5720336437225342, 0.40904033184051514, 0.2813834249973297, -0.16447286307811737, 0.8072209358215332, -0.10477064549922943, -0.08135844022035599, -0.15593576431274414, 0.3260035514831543, 0.13989140093326569, -0.2406539022922516, -0.01399514451622963, -0.09932410717010498, -0.3299522399902344, 0.019149884581565857, 0.37284332513809204, -0.3830850422382355, 0.32511577010154724, -0.20858535170555115, 0.09632308781147003, 1.028152346611023, -0.2796862721443176, -0.4141344428062439, 0.7638458609580994, 0.285861611366272, 0.765351414680481, 0.02670157700777054, 1.28118097782135, 0.20854245126247406, 0.12644481658935547, -0.10531897097826004, 0.3656612038612366, 0.8251111507415771, -0.3883831202983856, -0.11845394968986511], [1.7257099151611328, -0.09686405956745148, 0.2549608051776886, -0.08402881026268005, 0.9081313610076904, -0.045221827924251556, -0.10973131656646729, -0.11799690127372742, 0.42579710483551025, 0.16016271710395813, -0.197782963514328, 0.006474383175373077, -0.17534798383712769, -0.30738720297813416, 0.20188552141189575, 0.3432157635688782, -0.5862448215484619, 0.06390184909105301, -0.08942656219005585, 0.1266741156578064, 1.1967114210128784, -0.28889620304107666, -0.31064969301223755, 0.9053964614868164, 0.30861470103263855, 0.8902838230133057, 0.22831083834171295, 1.5892046689987183, 0.056501615792512894, 0.15265941619873047, -0.1321353018283844, 2.3959872722625732, 0.7801824808120728, -0.3850840926170349, -0.14809373021125793], [0.880490243434906, 0.1841939240694046, 0.22664640843868256, -0.31266504526138306, 0.7750216722488403, -0.16766349971294403, -0.01957259327173233, -0.10219667106866837, 0.2411510944366455, 0.13649217784404755, -0.3186916410923004, -0.061880744993686676, -0.04234674200415611, -0.2881196141242981, -0.041656870394945145, 0.3707078993320465, -0.3544560968875885, -0.29913094639778137, -0.21544751524925232, 0.08440525829792023, 1.4916898012161255, -0.33557459712028503, -0.3721104860305786, 0.7945544719696045, 0.08608418703079224, 0.7297157049179077, -0.08910644054412842, 1.0347620248794556, 0.11121638864278793, 0.19406437873840332, -0.15714967250823975, 0.38145989179611206, 0.809233546257019, -0.41484498977661133, -0.11625595390796661], [1.0341665744781494, -0.04065246134996414, 0.20810219645500183, -0.1951107680797577, 0.8242203593254089, -0.07076271623373032, -0.03589402511715889, -0.073029063642025, 0.3157278895378113, 0.1880079209804535, -0.2740875482559204, -0.030467666685581207, -0.03518315404653549, -0.24435898661613464, 0.12012271583080292, 0.3384397029876709, -0.48320096731185913, -0.48064735531806946, -0.13075976073741913, 0.07494916766881943, 1.4074102640151978, -0.3249712884426117, -0.29627618193626404, 0.9053964614868164, 0.07491104304790497, 0.8007801175117493, 0.08357014507055283, 0.9731572270393372, 0.04544561356306076, 0.2016505002975464, -0.2029416263103485, 1.9564993381500244, 0.7877291440963745, -0.3920746445655823, -0.22748491168022156], [0.9573283791542053, -0.20928725600242615, 0.1989634931087494, -0.3004973530769348, 0.8019896745681763, -0.09483389556407928, -0.006428943946957588, -0.10155990719795227, 0.24963359534740448, 0.13801579177379608, -0.3179912567138672, -0.03551725298166275, -0.01929876022040844, -0.32238972187042236, 0.008129604160785675, 0.4012579023838043, -0.3620424270629883, -0.11761455237865448, -0.16117139160633087, 0.03956309333443642, 1.1124318838119507, -0.3170088529586792, -0.3913601040840149, 0.7624388933181763, -2.8595328330993652e-05, 0.694166898727417, -0.1622856706380844, 0.9731572270393372, 0.1393485963344574, 0.1706562638282776, -0.13315895199775696, 0.3452306091785431, 0.8791214227676392, -0.41718149185180664, -0.038970593363046646], [1.3415191173553467, -0.09686405956745148, 0.19165056943893433, -0.19225193560123444, 0.883623480796814, -0.026996716856956482, -0.02730657160282135, -0.07361137866973877, 0.3391927480697632, 0.172858327627182, -0.26892322301864624, 0.004380801692605019, 0.016899578273296356, -0.3028830885887146, 0.15897910296916962, 0.3581286072731018, -0.4838809072971344, -0.11761455237865448, -0.13748884201049805, 0.08038445562124252, 1.32313072681427, -0.32643747329711914, -0.31014639139175415, 0.9053964614868164, 0.15184184908866882, 0.8126282691955566, 0.02495415508747101, 1.28118097782135, 0.09793537855148315, 0.14852267503738403, -0.17700184881687164, 1.6635074615478516, 0.8784723281860352, -0.3531252145767212, -0.12441796064376831], [0.573137640953064, -0.04065246134996414, 0.13988357782363892, -0.1923528015613556, 0.833498477935791, -0.13681164383888245, 0.1370447278022766, -0.13637501001358032, 0.26907289028167725, 0.10252563655376434, -0.3111465573310852, 0.02838250994682312, -0.005141801200807095, -0.34965771436691284, 0.021861303597688675, 0.45542076230049133, -0.3090013265609741, 0.9714838266372681, -0.163553386926651, -0.01789400912821293, 1.0702921152114868, -0.30796629190444946, -0.47190427780151367, 0.6840238571166992, 0.03408847004175186, 0.6990756988525391, -0.16486528515815735, 0.8499477505683899, 0.14101293683052063, 0.034678149968385696, -0.13327839970588684, 0.29014644026756287, 0.9406040906906128, -0.40369391441345215, 0.0993502289056778], [1.8025480508804321, 0.12798233330249786, 0.2084750086069107, -0.14377637207508087, 0.89091956615448, -0.08898621052503586, -0.10642813891172409, -0.08833081275224686, 0.36937788128852844, 0.12876704335212708, -0.304872989654541, 0.03740652650594711, 0.00913870707154274, -0.38007500767707825, -0.03771781548857689, 0.36490821838378906, -0.44574326276779175, 0.06390184909105301, -0.16935712099075317, 0.13034096360206604, 0.6067547798156738, -0.34904974699020386, -0.3501289486885071, 0.9053964614868164, 0.1859453022480011, 0.7415889501571655, -0.015689857304096222, 1.465995192527771, 0.23650851845741272, 0.07245547324419022, -0.11509411782026291, 0.6380358338356018, 0.9491248726844788, -0.34154173731803894, -0.06169477850198746], [3.7235019207000732, -0.15307565033435822, 0.3881089687347412, -0.15101408958435059, 0.9442024230957031, 0.05414610356092453, -0.3801802694797516, -0.03147052973508835, 0.48155444860458374, 0.15178918838500977, -0.2525634169578552, 0.01979202590882778, -0.01332903653383255, -0.39950552582740784, -0.08419273793697357, 0.30327093601226807, -0.6843926310539246, -1.0251965522766113, -0.16693858802318573, 0.344157874584198, 0.31177642941474915, -0.382135272026062, -0.2730143070220947, 0.5308759212493896, 0.44533589482307434, 0.7079031467437744, 0.04225432127714157, 2.205252170562744, 0.3902168869972229, 0.20835822820663452, -0.020413607358932495, 0.21558035910129547, 0.9361108541488647, -0.3665040135383606, -0.06466865539550781], [1.4951955080032349, -0.09686405956745148, 0.20462854206562042, -0.26277443766593933, 0.7952866554260254, -0.04694385081529617, -0.0772348940372467, -0.025853605940937996, 0.3164040446281433, 0.1125221773982048, -0.2757769823074341, -0.04605523869395256, 0.08098209649324417, -0.2981826066970825, -0.01802946627140045, 0.3166833221912384, -0.42337092757225037, -0.48064735531806946, -0.19734179973602295, 0.15067949891090393, 1.1545716524124146, -0.39266732335090637, -0.32065868377685547, 0.4570143520832062, 0.14361076056957245, 0.6259152889251709, -0.19176875054836273, 1.3427857160568237, 0.13213828206062317, 0.15899339318275452, -0.15201878547668457, 0.23455169796943665, 0.7831193208694458, -0.3070893883705139, 0.02044059708714485], [1.0341665744781494, 0.12798233330249786, 0.18885603547096252, -0.19739913940429688, 0.7039824724197388, -0.09444459527730942, -0.05571809038519859, -0.041539497673511505, 0.2902301251888275, 0.0907033383846283, -0.25839856266975403, -0.03646615892648697, -0.04378150776028633, -0.23213821649551392, 0.012108925729990005, 0.28620287775993347, -0.3830457925796509, -0.028348328545689583, -0.18572352826595306, 0.1264970600605011, 1.1967114210128784, -0.3615797758102417, -0.33696138858795166, 0.4605966806411743, 0.14124652743339539, 0.577785074710846, -0.08797744661569595, 1.0347620248794556, 0.13416670262813568, 0.10110142827033997, -0.17843613028526306, 0.22798369824886322, 0.6879469752311707, -0.2767118513584137, -0.009358992800116539], [2.186738967895508, 0.1841939240694046, 0.24234405159950256, -0.14377662539482117, 0.6698280572891235, -0.0621827207505703, -0.37583261728286743, 0.013359839096665382, 0.30943602323532104, 0.07439645379781723, -0.16570180654525757, -0.08803454786539078, -0.019965004175901413, -0.2273138016462326, -0.07535596936941147, 0.16308951377868652, -0.5109580755233765, -0.6621637344360352, -0.12521293759346008, 0.3243309259414673, 0.8595933318138123, -0.3559245467185974, -0.23784583806991577, 0.9053964614868164, 0.36425018310546875, 0.4861364960670471, 0.10173304378986359, 1.7740188837051392, 0.21667659282684326, 0.14012035727500916, -0.1568918079137802, 0.18977442383766174, 0.5328049659729004, -0.226109579205513, -0.07640089839696884], [0.6926895976066589, -0.37792205810546875, 0.11709900945425034, -0.04128975421190262, 0.5036100745201111, -0.10299365967512131, -0.07178797572851181, -0.09281737357378006, 0.2671230137348175, 0.08322493731975555, -0.10691516101360321, -0.052914801985025406, -0.03083566389977932, -0.22803428769111633, -0.005158793181180954, 0.18675357103347778, -0.3351444602012634, 0.4269346296787262, 0.05420516058802605, -0.04781915619969368, -0.5310187935829163, -0.27879202365875244, -0.343798965215683, 0.28373265266418457, -0.05203522741794586, 0.2337685078382492, -0.23157434165477753, 0.29550501704216003, 0.09876364469528198, 0.020417485386133194, 0.011273272335529327, 0.23445749282836914, 0.40321606397628784, -0.2037247270345688, 0.045154035091400146]]
"""

#Obtain Patient ID
patient_ids = []
for filename in os.listdir('./raw/set-a'):
    # the patient data in PhysioNet contains 6-digits
    match = re.search('\d{6}', filename)
    if match:
        id_ = match.group()
        patient_ids.append(id_)


attributes = ['DiasABP', 'HR', 'Na', 'Lactate', 'NIDiasABP', 'PaO2', 'WBC', 'pH', 'Albumin', 'ALT', 'Glucose', 'SaO2',
              'Temp', 'AST', 'Bilirubin', 'HCO3', 'BUN', 'RespRate', 'Mg', 'HCT', 'SysABP', 'FiO2', 'K', 'GCS',
              'Cholesterol', 'NISysABP', 'TroponinT', 'MAP', 'TroponinI', 'PaCO2', 'Platelets', 'Urine', 'NIMAP',
              'Creatinine', 'ALP']

mean = [59.540976152469405, 86.72320413227443, 139.06972964987443, 2.8797765291788986, 58.13833409690321,
		147.4835678885565, 12.670222585415166, 7.490957887101613, 2.922874149659863, 394.8899400819931,
		141.4867570064675, 96.66380228136883, 37.07362841054398, 505.5576196473552, 2.906465787821709,
		23.118951553526724, 27.413004968675743, 19.64795551193981, 2.0277491155660416, 30.692432164676188,
		119.60137167841977, 0.5404785381886381, 4.135790642787733, 11.407767149315339, 156.51746031746032,
		119.15012244292181, 1.2004983498349853, 80.20321011673151, 7.127188940092161, 40.39875518672199,
		191.05877024038804, 116.1171573535279, 77.08923183026529, 1.5052390166989214, 116.77122488658458]

std = [13.01436781437145, 17.789923096504985, 5.185595006246348, 2.5287518090506755, 15.06074282896952, 85.96290370390257,
		7.649058756791069, 8.384743923130074, 0.6515057685658769, 1201.033856726966, 67.62249645388543, 3.294112002091972,
		1.5604879744921516, 1515.362517984297, 5.902070316876287, 4.707600932877377, 23.403743427107095, 5.50914416318306,
		0.4220051299992514, 5.002058959758486, 23.730556355204214, 0.18634432509312762, 0.706337033602292,
		3.967579823394297, 45.99491531484596, 21.97610723063014, 2.716532297586456, 16.232515568438338, 9.754483687298688,
		9.062327978713556, 106.50939503021543, 170.65318497610315, 14.856134327604906, 1.6369529387005546,
		133.96778334724377]

time = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", 
		"12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", 
		"24:00", "25:00", "26:00", "27:00", "28:00", "29:00", "30:00", "31:00", "32:00", "33:00", "34:00", "35:00", 
		"36:00", "37:00", "38:00", "39:00", "40:00", "41:00", "42:00", "43:00", "44:00", "45:00", "46:00", "47:00"]

fileName = "./json/imputations.txt"

#Find imputed data
if os.path.isfile(fileName):
	print("File exists")
	file = open(fileName,"r")
	for id_ in patient_ids:
		line = file.readline()
		#Create outfile
		outfile = "./imputed_format/" + id_ +".csv"
		print("Processing " + id_)
		x = open(outfile, "a", newline='')
		csv_writer = csv.writer(x)
		#Write header
		csv_writer.writerow(["Time"] + attributes)
		#Reads imputed data
		line_details = line.replace("[[", "")
		line_details = line_details.replace("]]", "")
		line_details = line_details.replace("\n", "").split("], [")
		#line_details is array of size 48 hours. Each hour index contains 35 attributes which need to be scaled
		#obj = 35 attributes
		#evals = 35 scaled attributes
		counter = 0
		for obj in line_details:
			evals = obj.split(",")
			for i in range (35):
				evals[i]=(float(evals[i]) * std[i]) + mean[i] #Perform reverse scaling
			csv_writer.writerow([time[counter]] + evals)
			counter += 1
	file.close()
	x.close()
else:
    print("File does not exist")