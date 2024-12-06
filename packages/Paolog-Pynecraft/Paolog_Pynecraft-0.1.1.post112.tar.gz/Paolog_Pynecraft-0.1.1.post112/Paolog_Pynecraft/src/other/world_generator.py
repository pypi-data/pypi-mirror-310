import random 



from perlin_noise import PerlinNoise 







from                            .                           get_config_path import get_pynecraft_config_path as conf_path 





from 								.								world_status import WORLD_GENERATOR_STATUS 





from threading import Thread 







import os 









import codecs 







(                            IlI1lll1 													,													I1lII1lI                              ,                             ll1111lll11Il1l1 																,																lI111l11 																,																ll1II1I1                  ,                 I1IlIll1                    ,                   IlIl1lIl 									,									ll1lI1                 ,                lI1Ill1l                      ,                     llI1I111                            ,                           I11IIllI                         ,                        lI1IlI1I 														,														lll111II 														,														llll1II1                                 ,                                llllIIll                 ,                lI1Ill1l1Il1l1I 								,								I111l1ll                       ,                      IIII1l1I 										,										Ill1II1I1l1II1                      ,                     IIIlI11lllIl                                 ,                                lI111Il1l1 																,																lI1l11ll 									,									lIll1I11                   ,                  I1I1II11                 ,                l1l1ll11                          ,                         IIl1I1I1                                ,                               llIl1I1l                          ,                         I1ll11lI 														,														Il1IlI1ll                               ,                              II1Illl1                     ,                    l1II11Il                             ,                            IIIl1l1I                     ,                    II1I1IlI                                ,                               l1lIIlII                        ,                       I1lIII11                      ,                     llI1l1ll                               ,                              lIIlllI1 													,													llII1lI1                 ,                lIIl1III 														,														l1lIIIll11II 											,											l1l1l1ll                     ,                    IIll1llIlI111I11I1                 ,                I111IIIlI111I11ll                             ,                            I1l1ll1Il111I1                                 ,                                llIIl11I                 ,                II11ll1IlI                   ,                  IIl111l1                 ,                Il1lI11I 														,														lllII1Il 										,										II1l1II1 															,															II11ll11Ill                       ,                      l11lI1Il 											,											lI111lII 															,															I1I1II1I 														,														l1Ill1I1 									,									Il1l1Illl11l1 															,															lI1llIl1 														,														I1IIl1Il                              ,                             Il111II1 													,													II1I11Il                          ,                         I1111l1l                      ,                     I1IlIlll11IIl1lII 															,															IlII1l1l 										,										lIIIl11I 															,															I1l111I1 													,													lII1IIIl                  ,                 I11IlllI 									,									lIlI111lII1II1ll                               ,                              IIlIlIl1                          ,                         lIIlIlIIlIlllIIl1 													,													llI1111I 													,													lllll1Il                   ,                  lI11IlII                    ,                   IlI1II1I 															,															lIllI1l1                        ,                       Il1lIl11                       ,                      IlIIIlI1 													,													IIIl11ll1l11lll11l 												,												lllI1IlI                      ,                     IIIlI1IIII1 														,														IlllI1Il 																,																I1I11111 																,																Il11l1ll                 ,                IIIlI1I1Il11                      ,                     IIIl1ll1 														,														I11I11l1                    ,                   Il1lIl1I                  ,                 lII1lIll                               ,                              I11ll111II                          ,                         lll1Il11                          ,                         II11l1I1 																,																lI1lII1l                         ,                        I111lII1                    ,                   ll1IIIl1Il 														,														lllI11I1                   ,                  Il1l1ll1 												,												l1III1l1                          ,                         IIlI11II 															,															l1IlIl1I 									,									Illl1Il1 														,														Il1I1ll1                            ,                           lIIlI1IIIIIII1                                ,                               l1I1I1II 													,													III1lIlI1llI1l 													,													II11IIll                         ,                        IIIll11ll1lIl1I11 									,									l1III1Il                               ,                              I1l11ll1 									,									I111ll1l                                 ,                                IlI1IIIlIlI1I11l1llI                     ,                    llII1lll 												,												l111lIl1                                 ,                                I1lI11ll                       ,                      lI1III1l                                ,                               lIIIlllI                            ,                           II1lll1l                  ,                 I1lIl1lI 														,														Ill1I11                            ,                           ll1lIlI1 												,												lI11ll1lII1l 															,															lIIl1IIl                              ,                             II1Il1Il 																,																lIlI11lI                 ,                IIlll1II                               ,                              lIIIIlll 												,												I1ll1I1l 												,												IIlI111l                           ,                          IIIl1llllIl1I11Il 															,															IIlIIIIl                 ,                lII1IIII 															,															II11I11I 													,													Il1ll11I                   ,                  lIllI1II                           ,                          lI1l11I1                                 ,                                IlIllIIlI1 									,									l1lIIl11                    ,                   l1lII1l1 														,														IIlI1IlI 												,												I1IIl11l 												,												I11IIlI1                   ,                  ll1l1lll 															,															Illll1lI                             ,                            I1l1llIl                                 ,                                Il1l111lIl                   ,                  lI1l11lIII1ll 								,								I1l11lI1                       ,                      lI1l11l1 														,														lI11Il11                  ,                 IIlI1lI1 													,													lIl11111 																,																IlI11II1 									,									I1ll1ll1 														,														I11l1I1l 													,													IlI1Il11 														,														Il1I11l1 													,													l11I1llI                             ,                            I1llllIlIIl1II 												,												l11lIl1I 										,										IIlI1Ill 													,													l1I1I11l                    ,                   ll1III                     ,                    I111I1II 											,											IIl1l1Il                   ,                  IlIl1III                              ,                             Il1111Il1IlI1l                          ,                         IlIlIIll                        ,                       ll11lIII 								,								IIll11lI 								,								I1lll1lI                          ,                         llI1Il1ll1I1l1I1IIll                           ,                          l1lllI1I 													,													l11lI11I                                 ,                                IIlIll1l                        ,                       llIIl1l1 											,											llIIl11IIlllIl1 									,									l1lIlII1                      ,                     l1IllI1I1l1lIlI1l                      ,                     IlI1l1l1 											,											lIl1l1Il 														,														IIIIIlIl 													,													II1I1l1l 															,															I1lI1I1l1Ill1 										,										IlI11Ill                               ,                              llll1lIl 										,										I1lI1l11 														,														I1l1Il1l1lIl1IIl 															,															llll1111                     ,                    IIl11I1l                      ,                     lI1IlIll                              ,                             llIllI111111111 															,															I1lI1lI1l1lIllI                   ,                  lIllIIII                           ,                          l1IIll1I                               ,                              IllI1II1 																,																I1IIl1I1                    ,                   l11lII1I                      ,                     I1lIlIIl 														,														llIl1Ill 												,												llI1lII1                                 ,                                IllIIl1I                       ,                      I11I11II                       ,                      l1lll1I1 												,												llII111l                   ,                  I1lllIll 															,															II11l1lI                              ,                             lll1II1I 																,																l1I1l1l1                                ,                               I1Ill1 																,																Illll1Il 								,								Il1IIllI                               ,                              l1IIlIl1 											,											ll11l1I1ll1III1 									,									I11I1I1111lIlI1lII1                             ,                            l1lllIll                    ,                   IlI1lI11 										,										ll1l1111 																,																III1Il1I 											,											IIIlIl1lIl1lll1l1I1l                             ,                            I1111lI1111Il1lI11 											,											l1lIIlll                          ,                         II1l1lIl11l1II                              ,                             II1I1Il1 																,																Il1III1I                     ,                    I1I111IlI111I1lll                     ,                    II1IIl1l                                 ,                                IIllIll1                               ,                              lIl1llII 														,														lII1ll1l                            ,                           l11lI1II 											,											II11Ill1l 														,														Il1Il1IIlII11II1I 												,												Il11l1Il                    ,                   I11I11l1l1l1 															,															I1l1l11I 															,															lI1II1l1 													,													I1lllllI 									,									l1I1I1lI 												,												ll11l11l 															,															IlllI1I1                             ,                            IIIllIl1                         ,                        II1lll1I                    ,                   IIlIllI1                    ,                   llIl1IIl 													,													IIIl1Il1                     ,                    lIl11lllIlll111Il                       ,                      IIIIIIl1 															,															llII1Ill                            ,                           IIllIIl1                        ,                       l11I1lIl                             ,                            I1lI1I1l1lI1l1IlI                              ,                             IlIIllIlI11                        ,                       lIIlIIII 													,													IllI1lIl                                 ,                                ll1I1IlI                       ,                      IIIIl1lI                       ,                      lllI1lll 																,																l1Il1III                              ,                             ll11lIll                               ,                              Il1IlIll                       ,                      lIIII1III111                   ,                  I1lI1I1l 												,												I11111l1 																,																llIllI1l 														,														l11lIIl1                               ,                              lI1I1l11Ill 										,										I11Il1 														,														II1I1lll 											,											IIlII1lII1IllI1I 											,											ll1l1I 																,																l1II1lII 														,														I1IlI1l1                                ,                               IlI11ll1II                                ,                               l1llIIlI                                 ,                                IlIII1II                 ,                lIll11l1                                 ,                                Ill1111I                              ,                             lI1II1I1 															,															lII1I11l 																,																ll1l111l                              ,                             Il11IllI                               ,                              l1l1111lI1IIl1ll11                       ,                      Il1IlI11                         ,                        l1ll11Il 																,																lllll11I 										,										lI1IIllI 																,																lI11lIll 												,												lII1lI1l 															,															lI111I1lllI                          ,                         I1Il1lII 															,															l11l1l1l 											,											l1lI1ll1 								,								Il1ll1l1 															,															l1lI1l11                      ,                     lI1l1Ill 															,															lI1lIIll                                ,                               IlllI1II 														,														Il1llllI                   ,                  lIIlI1I1                              ,                             lII11II1lllllI1lI 													,													lIlI1II1I11I11l                               ,                              II1Il11l 																,																Il1llIl11I1IIl1                 ,                IllI11llII1 										,										I1l1I1II                          ,                         l1IllIl1                          ,                         II1llIlI11ll1I 										,										lll1lI1l                          ,                         Ill1I1I1                      ,                     IlIIllIl                             ,                            l111IlIl                 ,                lIllllI11lIIl1l1lI                                ,                               I1Il1lll 											)											                 =                 																(																                          (                          225363901                    ^                   76268526                       )                      											-																			(								99935323 												^												202498168 										)																				,																					~											                            -                            289389965                                 ^                                																~																                           -                           289390014                          ,                         415054154                        +                       															-															402477560                               -                                                         ~                           														-														12576587 													,																					~																						-														118133836                      -                     															(															227041910                   ^                  176354871 											)																								,													98564085 													^													335712223 									^									                         (                         560566687                                 ^                                817162646 																)																																,																								~								                    (                    250158971                                +                                                       -                        250159012                         )                                           ,                   range                                 ,                                                           (                           272569253                         ^                        827246029 															)															                   -                   									(									149039651 											^											697564280 									)																					,												679157996 											+											125961531 														-																							~																					-												805119500 												,												129834792                                +                               836376796                    +                                   (                790578730                      -                     1756790278                                 )                                                         ,                         													(													929625833 																^																908645912 												)												                      -                                        (                  539090044                 ^                560069799                           )                          									,									447636900 												+												195268698                            ^                                                         (                              153689422                 ^                796453022 														)														                    ,                    											(											207650342 											^											254910865 										)										                -                														(														885397450                        ^                       932694102 											)											                              ,                              															~																													-														593869997 								-								                  (                  996793560                           ^                          403464357                         )                                                      ,                              331378346                            ^                           524477139 												^												249620833                         +                                         -                 39738615                 ,                												~												                   (                   55326712                     +                    													-													55326749 									)																					,																						~										                               (                               158973278 											-											158973299                                 )                                														,														138174885                    +                   362865211 														+																										-																									(													813387660 															^															765856850 															)															                              ,                                                       ~                                           (                  698737626 												-												698737660 									)																									,																																~																                               -                                                              ~                                                     -                      52                                ,                               123172745 														^														775638678 											^																											(																66467155                 ^                714738753                   )                                                ,                                                    (                      485128108                    ^                   355099716 																)																                     -                     												(												591687397 												+																							-											428104457                                )                                                               ,                                													(													263791629 									^									1000921976                              )                             																-																                              (                              253581143                          ^                         990685260                             )                                                ,                    codecs                            .                           decode                                (                               'OnfvpJbbqOybpxCynaxf'                        ,                        'rot13'                  )                                             ,                           list 									,									                               ~                                                         -                          															(															734522489                          ^                         734522452                         )                        											,																						~											                         -                         															(															738695063                              ^                             738695101                  )                 								,								31230208                           ^                          467822560 													^																											~														                 -                 440332014                               ,                              275983731                           -                          72034182 										^										                  (                  868805716 														^														1071704490 													)													                       ,                       676695414 																^																273964380                            ^                                            (                 368745163                   ^                  771443448 									)									                           ,                                                    (                         752187418                                 ^                                711365239                  )                                      +                     										-																							(													163242293                            ^                           252250898                            )                                                   ,                        57734939 										+										589780169                        ^                       420247389 																-																													-													227267734                 ,                275651837 								-																					-													78227502                      ^                                     (                202584192 											^											419755436                      )                                                  ,                                                 ~                    																-																55018993 								^								                              ~                              															-															55018971                   ,                  235661044 									^									961223726                    ^                   														~														                                -                                927005429 											,											82072305 										^										581028173                       ^                                      (                428838462 											^											1070208431 									)									                 ,                 															(															542481329                     ^                    977857837 															)															                    +                                                -                                                        ~                            													-													438138481                     ,                    ''										[																			:									                    :                                        -                    1 									]									                 ,                 901744617                       ^                      496774179                              ^                                                 (                    279523700                   ^                  948607653                             )                                            ,                                              (                              37163837                        ^                       241703945                    )                                              +                                              -                   															(															557871418 										^										757039085                    )                   															,															                        ~                                                     -                                                            (                               259131646                          ^                         259131601                             )                            															,															0.1                                 ,                                                               ~                                                        -                                             ~                    											-											30 												,												                     ~                                                     -                                239961536                 ^                                       (                       948568346 									^									919045258                        )                       								,								432655409                        +                       79745974                             +                                                            -                                                ~                															-															512401345                  ,                 811987408                            ^                           642961265 											^											881249135 										-										508529869 											,											15785911                     -                    										-										356652005 														^														505080891                    -                   132642951                               ,                              846039940 																^																930271094                   ^                  										(										962430327                               ^                              1011007894                    )                                     ,                  71805570                                -                               													-													626231734                         ^                        914707624 															+															                                -                                216670367 									,									                    ~                                                -                            																(																762639778 											^											762639797 													)																													,																'w'															[																												:													                          :                                           -                 1                           ]                          								,								                     (                     741681697 															^															47476198 														)																													-																															(																643557751                   ^                  146452150                             )                            												,												915399414 											+											                    -                    208611169 													+													                     -                                                   (                              203940272 																^																638016054                      )                                     ,                									(									922860651 												^												13580041                            )                           												-												                ~                												-												936282939 													,													codecs 											.											decode 																(																'/jbeyqf/{}/vasb.gkg'                 ,                 'rot13'																)																                         ,                         codecs 								.								decode 												(												b'476c617373426c6f636b'													,													'hex'                    )                                        .                    decode                    (                   'utf-8'															)															                           ,                           												~																					-																			(										230669799                       ^                      230669793                            )                                                     ,                          										(										379408187                                ^                               1002881090                              )                             											+																			(								35700260 															+															                     -                     796675479 										)																					,											                             (                             558437737                      ^                     98438531                             )                            															-															                     (                     948267227 												-												334385155 								)																								,																                             ~                             														-														449701055                               ^                              718128648 													+																								-											268427643 									,									786690876 									^									154659432 															^															491241389 													-													                   -                   176970134                             ,                                                         (                             540601314                  ^                 364337238                   )                                               +                             									-									                               (                               661660586                         ^                        318738458                              )                             															,															961324354                       ^                      594431068                           ^                          655392423                               +                              										-										216896914                             ,                            0.05 								,								380673036 											^											814591133                          ^                         											(											830035204                    ^                   390358453 									)									                      ,                      940932764 											^											49030686                              ^                             366339558 															-															                     -                     623080178 													,													663962288 													-													589848622                        ^                       615060201 																-																540946489                            ,                                             ~                                      -                                                 (                             999271622                       ^                      999271648 									)																			,																										~																								-																	(									949500534                       ^                      949500504                                )                               								,								354347625 															^															233561089 											^																						(											640053544                   ^                  1054033752                      )                                       ,                                           (                         767520351 											^											757691081 												)												                     -                     													(													586378899                         ^                        577073901                               )                                                          ,                            796355302 													+													                        -                        252316822 									+																	(								628928596 															+															                     -                     1172967048                                 )                                											,											                         ~                         																-																665839339                             -                            												~																									-													665839293                     ,                    808886905                    -                   497010192                             -                                                        (                            503309235                           ^                          258555780 											)																									,																													(															723275400                     ^                    285464660 												)																										-														                      (                      97966585                   ^                  1070157626                                )                               									,									                              ~                              														-														                       (                       198672461 																^																198672474 												)																											,															334641765                        +                       113778252                    ^                   										(										383400289 									^									207643132                               )                                                        ,                                                        ~                                                  -                    										~										                        -                        23                  ,                 																~																																-																                     (                     64002090 												^												64002080                         )                                                  ,                          191822398                  +                 586888426                         +                                                       -                                                    (                     170320434 																^																609013011 															)																							,								624269427 												^												860493024                         ^                        										~										                                -                                377457799 								,								523726461 																^																793047053                           ^                          												(												682512466 									^									417189431                             )                                                      ,                          289320342                       ^                      902770433 												^																					(									231343094                           ^                          691765577 														)														                ,                620583508 													^													893917369 													^													928765228                                -                               631673411                               ,                              											~																				-																			(										344185463                  ^                 344185434                         )                        															,															283419534                   +                                        -                      244240027 														+														                              -                                                    ~                                                -                          39179499                    ,                   codecs 											.											decode                 (                ' \n'													,													'rot13'                          )                          											,																				~									                -                836357435 																^																                        (                        889805045 															^															80778707                          )                         									,																						~																													-																498717865 											+											                -                															(															639011868 									^									1001347182 									)									                         ,                         									~																		(									412289004 								+								                  -                  412289013                      )                                                     ,                                                               (                               395268468 											^											925081372 														)														                    -                                                 (                             452151147 																^																979339613                                 )                                                         ,                         545718799 										+										60422333                    -                   													(													866076922                       ^                      398438992 												)																											,																									~																									-															739664124 									^																								(															827524281 												^												491086944 											)																				,																				~											                   -                   372758606                       ^                      												(												50712740 												^												355600584                          )                                                ,                                                      (                               715730809 																^																972082678                      )                                                     -                                														~														                       -                       324657769 																,																140993777                      ^                     436008942 													^													146566746                        -                                                     -                              148841657 																,																																~																																-																                (                758638757 												^												758638783 									)									                  ,                  627259492                        ^                       566104521 								^																						(														760817472 												^												696520400                                )                               															,															639006670                            +                           169087126 											^																										~																														-															808093815 								,								997372595                  +                 														-														419566359                                 ^                                                (                299706210                              ^                             867023034 													)													                          ,                          572255868                                ^                               220594187                    ^                   										(										943901410                     ^                    394208398                                 )                                                            ,                            range 														,														605714975 											+											                             -                             57199404                               ^                                                           (                             298687275 													^													830223867 								)																						,														                            ~                            										(										540954723 																+																									-									540954742 																)																                            ,                            385950737                                 +                                2118813                             +                            													-																								~											                   -                   388069450                          ,                         227859466                   ^                  1047552677 											^											272579252                             -                                                           -                               598049799                         ,                        															(															878282087 											^											209415545                            )                           											+																			-								                 (                 994315726                         ^                        57076340                                )                                                      ,                       codecs 								.								decode 									(									b'772b'                              ,                              'hex'										)										                    .                    decode 																(																'utf-8'                  )                                              ,                            198037678 											+											347675322                          ^                         662598215                      +                                      -                 116885300                               ,                              902443237 											^											412272719                         ^                        880311616 										+																						-												119506074                             ,                                                   (                       907223108                    ^                   411382178                       )                      									-									                             (                             567035863 								^								257578506 								)								                             ,                             ''									.									join 										(										                            [                            chr 													(													Il1lI111                      ^                     8555 								)								for Il1lI111 in                                [                               8504                      ,                     8479                  ,                 8452 											,											8453                                 ,                                8462                             ,                            8489 												,												8455 											,											8452 													,													8456 												,												8448 															]															                    ]                    									)									                    ,                    																~																										-										                   ~                                                   -                                35 													,													                  ~                                           -                         														(														9809692 										^										9809688                  )                                  ,                 											(											255009211 																^																665803994                     )                    								-								                     ~                                              -                         681344344                         ,                        0.2 								,								542395077 													+																										-													256892933                             ^                            797451386                 +                                             -                             511949224 											,																										~																									(										545616612 																+																												-												545616665 														)														                              ,                              548273329                               ^                              1009217658                      ^                     791450831 															-															312608762                        ,                       663078568                           +                                                     -                           317037907 														^														                (                50492467 									^									396516712                               )                              														,														                     ~                                            -                       957477199 												^												186178855 												+												771298392 													,													903553550 												+												                             -                             797221327 															+																														-																							(								9558076 															^															113727506 									)																				,																			~								                        -                        76814892 								-								                       (                       131825721                            +                                                       -                            55010842                  )                 															,															348556044 									^									3115379 											^											56587385                              -                                                       -                          294227423 													,													312190775 													-													                       -                       632114439                          ^                         								(								571442130 											^											440891362 																)																                             ,                             763434181                              ^                             951391426 																^																467270143                            +                                                   -                        111540710                               ,                              760040899 														^														393365584 										^										460111692                       +                      517097031                         ,                        											~																					-										850697567 												-																									(													828789637                    +                   21907908 											)																					,										676544545                    ^                   754805896 												^																											(															61364929                                 ^                                117864035 								)								                      ,                      215906158 									^									230964589 															^															                     (                     706587610 										^										721936888                 )                														,																							~																						-													760735989                  ^                 								~																	-									760735987                          ,                         																~																                         -                         13430893 																+																                       -                       													(													50872458 									^									63221998                     )                                           ,                       548958815                      +                     233589775                        +                       								-								                  (                  299134395                               ^                              1064358894 															)															                          ,                          193579670                       ^                      212252198 															^															                 ~                 															-															120552599 										,										                               (                               287763626 											^											308290728                       )                      									-									                    ~                                            -                        54970366 								,																								~																													-													492740015 														-														                              ~                              													-													492739984 								,								140355353 																^																376823960                 ^                384529239 														-																									-											121426992 								,																			~																				-																							(														775432722 																^																775432704 																)																                ,                339348119                    ^                   818455474                               ^                              																~																												-												619882768                               ,                                                    ~                      													-													                      (                      94266123 													^													94266131 										)										                             ,                             196249755 																-																											-											728179238                             ^                                                    (                        15912310                        ^                       938174364                                )                                                  ,                   										(										390812560                            ^                           489948225                               )                              															+															                               (                               967249077                           +                                               -                     1143366788 										)										                            ,                            										~																				(										446397548                                -                               446397588                         )                        												,												                    ~                    								-								                  ~                  										-										50                            ,                                                    ~                         															(															834464528 											-											834464534                         )                        																,																codecs 												.												decode                                (                               b''													,													'hex'															)																											.												decode                 (                'utf-8'											)																				,									954001666                            ^                           63747112 												^												                             (                             140891663                              ^                             863341434 											)																			,								                          ~                          													-																					~																							-															50 									,									742530578 													^													72200238                             ^                                                (                    861690249                       ^                      458487698 														)																								,										829060153 															^															642361899                       ^                      														(														911823796                         ^                        561679746 										)																										,																int 								,								689849135                      +                                       -                  452076545                                 -                                												(												769027892                 ^                603615291 									)																									,																66881520                        ^                       548365465                              ^                             246087024                               -                                                    -                      346613254 								,								832603145 													-													                  -                  98607775 													^													                             ~                             								-								931210882                        ,                       								(								279976657                   ^                  492216444 												)												                    -                    								(								286320199                            ^                           485907656                            )                           										,										411703147                   ^                  464807208                          ^                                                    ~                                                -                     54424153                           ,                                                      (                            922835477                            ^                           601496506 								)								                    -                    										(										185354129 																+																164559357 											)											                              ,                              pow 															,															                           ~                           											(											763458569                       +                      												-												763458610 										)										                             ,                             170396276 																^																28123609 														^														                       ~                       								-								193276861                       ,                      301530475                 +                390731936 										+																					-																					(										346241132 																^																1038101942                        )                                          ,                   533770676                           ^                          1054432621 														^														913888965                              -                             359590400                     ,                                            (                        524753375                            ^                           526792473 																)																                -                                                (                                467570557                                ^                               469737912                 )                                 ,                 99986737                        -                       															-															455331428 													^																									(												472113059 									^									1027253265                                )                               																,																str                        ,                       codecs 													.													decode 																(																b'44454255475f43484f434f4c4154455f43414b455f424c4f434b'											,											'hex'										)										                  .                  decode                     (                    'utf-8'								)																								,																								~								                   -                                              (                           568386035 														^														568386016                    )                   													,													39177310 														^														854387859                               ^                              747080454                     +                    70358461                          ,                                                        ~                                                            -                             24505168 													-																								(											276852298                     ^                    301303167                    )                                       ,                    															~																										-																										~																												-													12 												,												593085822                                ^                               613045402                               ^                                                             (                               265885340 															^															134907759                 )                												,												15063392                              ^                             656867978 																^																													(													971181930                   ^                  505533587                                 )                                													,																								~																										-															                              ~                                                           -                             22 																,																782523032 								^								724160485                    ^                   									(									890107122 								^								813719948                     )                    																,																																(																384719248 											^											392824045 												)																				+								                        -                        															(															223821208 										^										215179468 													)													                       ,                                             (                      285267930 													^													378563043                  )                                               +                                              (                933981253                                -                               1060907646 									)									                   ,                   'kcolBkcirB'                    [                                    :                														:														                            -                            1                        ]                       													,													0.5                              ,                             797784190                            -                           85672633 								^								73319462                             +                            638792111 												,												934243456                          ^                         1030081530                  ^                                             ~                                                        -                            181053295 											,											                         ~                                                    (                           32860257                       +                      												-												32860313 															)																								,									                           (                           187947311                           ^                          419435895                 )                								+																						(														788730386 														+														                   -                   1094114880                                )                                                ,                 codecs 																.																decode 													(													b'776f726c642e706377'														,														'hex'                        )                        										.										decode                         (                        'utf-8'														)														                          ,                          776185074 																-																154437213 												+												                          -                                                  (                        578965185                  ^                 126701732 											)																									,																									(											400052603                 ^                258821518 												)																												-																								(								557391317                       ^                      965476657                          )                                          ,                                  ~                 										-										963750899                  +                                             (                            841320915                               +                              													-													1805071797 								)								                      ,                      781009319                            -                                             -                  201420794 															^																															~																                                -                                982430140                     ,                    										(										13272124                    ^                   590981456                      )                                              -                         												(												916713999 									^									357621606                           )                          											,																			(								574121550                    ^                   123426367 									)									                       +                       												-																							~																											-																627257456 										,										19266904                     ^                    74858961                   ^                                   (                 612724523 													^													567727022 									)																							,														922266464 															-															431403199                    +                   														-														                    ~                    													-													490863221 															,															168127913 								+								28645328                                ^                               														(														539404177 												^												731652796                   )                  											,											454430462 									-																				-											17052728 											+																						(											902389810                           +                                            -                  1373872953                              )                             															,															261375449 														^														614692812                                ^                               										(										800043900 										^										77103463                 )                												,												929361148                       -                      406221444 									^									772602352 													-													249462740 								,								587121170                          +                         151358955                               -                                                          (                            457707588 															^															927752103                             )                            										,										909267851 										^										556628856                            ^                                              (                   447173788 																^																230194303                           )                          																,																                                (                                216087282                                ^                               143191255 								)								                       -                                         (                  643822318 										+																					-											569777390                      )                     														,														209476455                            ^                           748207198 													^													509595431                           -                          										-										42276888 										,										986009740 										^										940882039 										^										                           (                           712223009 																^																681722328                            )                           									,																			(										455661983 													^													249077995 										)										                           -                                                       (                            663373333 									^									846872386                        )                                                    ,                             263645870 											^											175407144                    ^                   567340250                              -                             470712892                 ,                640106107                    ^                   1055442286 													^																											(														84774824                          ^                         499283122                          )                         								,								648625847 								^								545429536                             ^                                                       ~                           													-													103523995                    ,                   563693979                     -                    													-													113425800 												+																				-								                      (                      673177491                           ^                          4446345                       )                      											,											495330011                        ^                       13011421 											^																											(																285870000 													^													206220453 										)																								,																							~																					-												487422697 												^												977665934                    +                                   -                490243233                 ,                978391479                           ^                          654026613                               ^                              368928169 												-												                   -                   112021789 															,															333571799 												+												2632264 											+											                     (                     914839447 												-												1251043479                         )                                                       ,                               int                               ,                              981018169                     +                    									-									935020682 												^												667061019 													-													621063552                            ,                           514641445 								+								232869671                           ^                          															(															488354137                            ^                           831892481 													)													                              ,                              														~														                 -                 318849947                  ^                 113128827 												-												                   -                   205721118 										,										                          ~                          														-														44952752                         ^                        329398520 															-															284445780                      ,                     int                  ,                 845123741 														-														50101952 														-																						(								349279652 																^																1001555052 																)																                        ,                                                    ~                            																-																                               ~                                                   -                    52 								,																							~															                                -                                																(																984440288                               ^                              984440262                             )                                                ,                                                   ~                               								-								687972012                              ^                             													(													698478961                   ^                  10514417                     )                    												,																								~												                        -                        240538616 									-									                (                737720441                              -                             497181851                 )                									,									384337828 														-														331357494                               ^                              303981666 									+																	-								251001421 									,									                                ~                                									-									297956794 											^											                   (                   344400340                       ^                      88429664                 )                                              ,                              														(														963128354 												^												942732249                          )                         												+																										(														955276291 								+																								-																977877990 									)																	,								414374067 								+								25794988                             -                            												~																							-											440169024 									,									                (                705176331                               ^                              136746650 											)																						-																										~															                  -                  573486453                          ,                         626846288                                 -                                                                -                                245472268                                ^                                                  (                   374293975                        ^                       632406950                             )                            												,												                        ~                                                   (                           915154563                      -                     915154600 													)																								,											                               (                               546947041                                 ^                                628401147                                 )                                                           -                                                          (                               400015374                      ^                     305847282 												)																									,																								~																				(									977084730 										+										                              -                              977084769                       )                      															,																												(													179127603                    ^                   1046141701 												)												                        +                                                        -                                                           (                           427941870 												^												762724826 																)																                         ,                         									~									                      -                      196849211 								^																								(																677276077                               ^                              602261400                       )                      								,								991015617                 ^                333274576                          ^                         365245992 										-										                           -                           319273227 													,													821992003 												+												                                -                                721148290 								^								                          (                          170717928 																^																204354059                                )                               												,																								~																											-															145612151                     ^                    488567480 										+										                       -                       342955325 																,																523515151 								+								                 -                 494823256 											^											                 (                 311425803                       ^                      322582165 									)																								,															                 ~                                              -                             355117803                            ^                                           (                883009820 													^													562758610                 )                                 ,                                 ~                                   -                   									~									                   -                   16 																,																									~																								-															                          (                          613274224 								^								613274209                          )                         												,												210504921                        ^                       147860783                        ^                                              ~                       											-											73146870                   ,                  486675572                  +                 488559436                               +                              									-																									(																491221660 															^															661099815 																)																														,														356109490                               -                                                    -                      119933068 												+												                             (                             256025865                        -                       732068389 										)										                               ,                               												~																										-														904573940                   ^                                           (                         907681292                           ^                          66104784                  )                                               ,                                              (                279877838 										^										1052012375                      )                                                +                                                          -                                                       ~                        													-													773519167                    ,                   858194097                               ^                              436036799                        ^                       										(										572631898                               ^                              150720378                 )                                          ,                          open 											,											                   (                   352813354                       ^                      304874469 												)												                          -                                                     (                           110799824 														^														28387610                       )                      												,												                   (                   226570925                     ^                    1020571377 										)										                          -                                                          (                                932835451 															+															                             -                             105141286                             )                                            ,                521173963                    +                   472618187 											^																							~												                  -                  993792182                        ,                                                       (                                827218793 									^									1070383701                    )                   								-								                    (                    729557480                          +                                                     -                            486117602                             )                            																,																50516806                                ^                               995402709 									^									                    (                    987823773                      ^                     45518346                           )                          											,																						~											                      -                      359274229                     ^                    										(										518716305 														^														192998721                          )                         												,																												(																615962376 														^														562064503                         )                                                     +                                                 -                                             ~                         															-															87473000                   ,                  231499744                        -                       105889363                              ^                                                     (                        308443118 								^								354344556 															)															                    ,                    516985296                      +                     174115135 														^														815345429 								-								124244977 										,																			(									299121604 								^								519004597 								)																	-																		~									                              -                              255547975                 ,                                      ~                      														-																											(													804955160                       ^                      804955198 								)																		,																							(													519166471 											^											854274074                            )                           																-																												(												936495426 													^													466297679 														)														                 ,                 												(												899957998 										^										727258034                   )                                             +                           																(																271005895 								+																							-															790925303                              )                             									,																			~																				-										497834564                         ^                                        (                948664198                     ^                    623324612                     )                    										,										                         ~                                                -                       600703613 												^																						(										667460693                          ^                         67544587                            )                                                     ,                                                ~                                                   -                             141304020 														^														                             (                             351301664 								^								480006387                              )                                                           ,                              759365718 														^														530445828                               ^                              														(														503436168                 ^                752821658                           )                                                   ,                         round 											,											64267161                    ^                   44608010                      ^                     585888116                     +                                          -                      560981956 															,															                     ~                     											-											373621733 										+										                     -                     												(												351744983 														^														45232180 														)																						,								453708035                              ^                             886800870                   ^                  403354063                       -                                                 -                           398841593 														,														                            (                            660056216                  ^                 401255283 														)																														-																									(									855988770                   +                                         -                       38295117                                 )                                								,								326745630 											+											398864521 											+											                   (                   311725101 								+								                      -                      1037335237 												)																				,								218149542 									+									578612902 									+									                       -                       															(															397387446 																^																953288602 									)																								,															codecs 													.													decode 															(															b'626967'                        ,                        'hex'										)																				.										decode 									(									'utf-8'                                )                                												,																				~								                             -                             8091502                 +                                        (                        558419311                     -                    566510781                   )                  																,																594313345                                 -                                89736799                      -                     											(											468288455                       ^                      100317663                           )                                             ,                   														(														292886306 										^										484642265 								)																	-									                                (                                539792737 										^										767201155 								)								                          ,                          														(														160809338                                ^                               1012124819                             )                                            +                															(															452985978 										+										                   -                   1355158079 														)														                          ,                          19401059                     +                    539183185                              -                                                     (                        816018032 														-														257433795                     )                    															,															147059332 														+														115266470 										+																							-																										(													779596236                       ^                      567637978                       )                      												,												codecs                   .                  decode                   (                  '/jbeyqf/{}/jbeyq.cpj'                               ,                               'rot13'                    )                                              ,                          range                        ,                       													~													                        -                        571338991 								^								96080203                 -                								-								475258788                            ,                           253137358 										^										579730180 													^													                   (                   241991034                            ^                           603396013 															)																									,										                            ~                            																-																226497084                                 ^                                                               ~                                                   -                    226497133 												,																									~													                   -                   																(																844556550                               ^                              844556633                   )                  												,												987290504 								^								460285328 															^															320839738 											-											                  -                  244850138                    ,                   int                    ,                   codecs                     .                    decode 												(												b'2f776f726c64732f7b7d2f'                         ,                         'hex'                          )                          															.															decode                        (                       'utf-8'                     )                                            ,                                                     ~                                               -                 806016625 																^																												(												788745773 															^															520722541                       )                      									,									                    ~                    									-																						(													115773006 											^											115773054                          )                                                       ,                              615319585 									^									927219316 													^													                       (                       598307691 											^											809518370                        )                                       ,                232984253 											+											368049556                 +                                       (                       653552000                         +                                                       -                               1254585776                  )                                        ,                                                  (                           399340329 															^															886775275 														)																														-																								(								398531010 											^											886536054                                 )                                										,										84955832                  ^                 765466472 								^								                   ~                   											-											682640864                   ,                                        (                      269600224                           ^                          19876162 									)																		-																						(													920045201                           ^                          669534949                             )                            															,															open                           ,                          																~																										(										237765008                                 +                                                         -                         237765051 										)																			,									                                ~                                											(											92226748                         +                        															-															92226787                              )                                                           ,                              104238883                          -                         										-										856831584                     +                                        -                                                   (                               125345308 									^									1043356536 								)								                                ,                                range                      ,                     242800495                     ^                    479111531 															^															                        (                        940243464 													^													721191967 								)								                             ,                             codecs 														.														decode 															(															'j+'																,																'rot13'                   )                   										,																								~																											-													                          (                          483172141                 ^                483172150 																)																												,												                        ~                                          -                  657455324 								+																				(												644077978                    +                   															-															1301533266                     )                                          ,                                       ~                 															(															301270163                      +                     																-																301270205                             )                                             ,                 265552354                     ^                    104047167                     ^                                    ~                                         -                         166175708 													,													                               (                               302470456                             ^                            1026486770                     )                                                  +                              														-																									(											217491204 												^												601817995                      )                                                ,                           									(									868251723                      ^                     748647016                     )                                                   +                               														-														                                ~                                                  -                  526322185                        ,                                          ~                   														-														                   ~                   									-									37 												,																						~										                       -                       197733504 													-													                 (                 780162892                   ^                  625572648 												)																											,															11944529                        ^                       249247796 																^																                               (                               509195631 											^											271896367                  )                 													,																						(									505152763                         ^                        37226408                                )                                                    -                     											(											381357804                 ^                178195909                               )                              																,																codecs                            .                           decode                  (                 b'426564726f636b426c6f636b'                             ,                             'hex'                                )                                										.										decode 														(														'utf-8'														)														                  ,                  								~																					(													133415835 										+										                       -                       133415862                                 )                                														,														945745086                         ^                        450923975 								^								                         (                         96924042 											^											662212831                               )                              												)												

def I1I1I1lI                        (                       l11lIllI                              )                                                          :                             








                       return True 



def IIlI11ll 								(								l11lIllI 															)																							:								








                       return l11lIllI 
IlllI11l 														=														lambda IIII1lll                     :                    True 




I11lI1lI 									=									lambda IIII1lll 												:												IIII1lll 


class lI1lI1l1lI1l1lll1II                   :                  


                       @								staticmethod 




                       def lIIlIl11 																(																llIllllI                         )                                                       :                               






                                              return True 

                       @                      staticmethod 





                       def llIIIIl1                  (                 llIllllI                            )                                                          :                               


                                              return llIllllI 









def l1111ll1                              (                             l1l1lIlI 															,															l111111l 															)															                   :                   







                       try 														:														









                                              return l1l1lIlI                               !=                              l111111l 
                       except 											:											
                                              return not l1l1lIlI 															==															l111111l 




def l11II1l1 								(								II1Illll                              ,                             I11I11I1                         )                                                      :                              


                       try 										:										

                                              return II1Illll 										>=										I11I11I1 
                       except 													:													



                                              return not II1Illll 								<								I11I11I1 









def lIlllIIl 																(																I1111l11                    ,                   l1Il11ll                         )                                                       :                               








                       try                         :                        







                                              return I1111l11                       <                      l1Il11ll 


                       except                         :                        

                                              return not I1111l11 														>=														l1Il11ll 






def lI1lI1Il11II1I 																(																lIl11lIl                  ,                 llII11ll 								)								                           :                           





                       try 																:																





                                              return lIl11lIl 											>											llII11ll 
                       except 										:										








                                              return not lIl11lIl 														<=														llII11ll 


def lI1Il11I 												(												IlI1llI11lI                 ,                IIl1l1II 														)																												:														


                       try 															:															









                                              return IlI1llI11lI 										==										IIl1l1II 

                       except                                 :                                






                                              return not IlI1llI11lI 								!=								IIl1l1II 









def lIlI11Il                     (                    I1lI1l1l 											)											                   :                   









                       I1lI1l1l 												.												progression                           :                          IlI11II1 								=								I1lI1I1l 

def l1IIlI                  (                 IllIll1I 													)													                   :                   




                       return IllIll1I                      .                     progression 









class WorldGenerator                    :                   



                       def __init__ 								(								self 											)																			:								









                                              return lIlI11Il 													(													self                        )                       










                       def generate_world 													(													self                          ,                         world_name 																:																str                   ,                  seed                            :                           str 										,										world_size                           :                          str 										)																								->														None 										:										




                                              (													I11l11Il 													,													ll1llIlI                              ,                             I1I1IllI 														,														Il1IlI1I 											)																										=															                         (                         world_size 													,													self                  ,                 world_name 								,								seed                        )                       
                                              I1IIl1II 														:														Thread                              =                             Thread 									(									target                        =                       ll1llIlI                          .                         __generate_world                          ,                         args                               =                              									(									I1I1IllI                           ,                          Il1IlI1I 															,															I11l11Il                      )                                                    )                               








                                              I1IIl1II 											.											start                     (                    													)													









                       def __generate_world 													(													self                       ,                      world_name                       :                      str                   ,                  seed 													:													str 								,								world_size                                 :                                str 											)																											->																None                             :                            







                                              (                  lll11I1I 									,									Il11l1111IIllI1llll                   ,                  l1ll1IlI 									,									I1II1l11 												)																										=																										(												world_name                             ,                            self 														,														seed                    ,                   world_size                        )                       

                                              Il11l1111IIllI1llll 													.													progression                     =                    l1lIlII1 




                                              try 								:								
                                                                     ll1IlI1l                          :                         IlI1lI11                  =                 lllll11I                     .                    from_bytes 													(													l1ll1IlI                                 .                                encode 								(																							)															                  ,                  l1II1lII 										)										




                                                                     I1l1l11l 													:													PerlinNoise                                =                               PerlinNoise 											(											octaves 														=														IIl11I1l                              ,                             seed 											=											ll1IlI1l                       )                      

                                                                     I111III1 									:									Il1IIllI 															=															Il1IIllI 															(															I1II1l11 											)											

                                                                     l1l1I1II 												=												llI1Il1ll1I1l1I1IIll 


                                                                     II1llI11 												=												llIl1IIl 



                                                                     if not lI1lI1l1lI1l1lll1II 										.										lIIlIl11 												(												I1lI1I1l                                 )                                                               :                               






                                                                                            II1llI11                              =                             llI1111I 









                                                                     else                              :                             

                                                                                            II1llI11 										=										Il11l1Il 
                                                                     if II1llI11                         ==                        Il11l1Il 								:								





                                                                                            if l1111ll1 									(									I111III1                     ,                    IIlI111l                      )                     													:													






                                                                                                                   II1llI11 												=												IIlI1IlI 





                                                                                            else                              :                             




                                                                                                                   II1llI11                    =                   llI1111I 



                                                                     if II1llI11                             ==                            I1lI1l11                     :                    


                                                                                            l1l1I1II                         =                        lIllI1II 
                                                                     if II1llI11 										==										l1lll1I1 															:															


                                                                                            l1l1I1II                          =                         I1lII1lI 

                                                                     if l1l1I1II 																==																lIllI1II 												:												


                                                                                            lIIlI11l                   =                  IIIl1llllIl1I11Il 

                                                                                            if not IlllI11l 											(											IIlI1lI1                 )                                    :                    
                                                                                                                   lIIlI11l                           =                          I1I111IlI111I1lll 









                                                                                            else 																:																



                                                                                                                   lIIlI11l 										=										II11ll1IlI 



                                                                                            if lIIlI11l                 ==                lI1III1l 											:											









                                                                                                                   if not IlllI11l 									(									IIlI111l 											)											                              :                              








                                                                                                                                          lIIlI11l 									=									I1l111I1 







                                                                                                                   else 																:																



                                                                                                                                          lIIlI11l                     =                    lI1l1Ill 




                                                                                            if lIIlI11l 															==															lI1l1Ill                    :                   




                                                                                                                   l1l1I1II                           =                          lI1Ill1l1Il1l1I 






                                                                                            if lIIlI11l                         ==                        ll1l1I                  :                 








                                                                                                                   l1l1I1II                  =                 I1lII1lI 








                                                                     if l1l1I1II                         ==                        lI1Ill1l1Il1l1I                        :                       




                                                                                            pass 




                                                                     if l1l1I1II 											==											lllII1Il 											:											









                                                                                            raise WORLD_GENERATOR_STATUS 											.											WORLD_SIZE_0 																(																                            )                            









                                                                     Ill1llIl                                 =                                IIIl1l1I 









                                                                     llllllII                       =                      I1lll1lI 







                                                                     if l1111ll1 									(									lll11I1I 																,																I1l11lI1 														)																										:												








                                                                                            llllllII 								=								IIIl1Il1 


                                                                     else 									:									

                                                                                            llllllII 								=								IIlI1lI1 






                                                                     if llllllII 									==									IIIl1Il1 										:										







                                                                                            if l11II1l1                            (                           lII1IIIl 																,																I1Il1lll                  )                 															:															







                                                                                                                   llllllII 								=								II1llIlI11ll1I 





                                                                                            else 																:																








                                                                                                                   llllllII 														=														IIlI1lI1 


                                                                     if llllllII 												==												IIlI1lI1 													:													




                                                                                            Ill1llIl 																=																lI11ll1lII1l 






                                                                     if llllllII                     ==                    II1llIlI11ll1I                     :                    






                                                                                            Ill1llIl 								=								llI1Il1ll1I1l1I1IIll 



                                                                     if Ill1llIl                  ==                 l1I1I1lI 														:														
                                                                                            l1lll11l 														=														lllII1Il 


                                                                                            if not lII1lIll 														:														




                                                                                                                   l1lll11l 															=															lI111I1lllI 


                                                                                            else 										:										




                                                                                                                   l1lll11l 																=																l1lll1I1 

                                                                                            if l1lll11l 										==										llI1111I                          :                         




                                                                                                                   if l11II1l1 														(														Il1III1I 														,														l1lIIIll11II                             )                                                         :                             
                                                                                                                                          l1lll11l                           =                          lI111I1lllI 








                                                                                                                   else 																:																

                                                                                                                                          l1lll11l                   =                  I1ll11lI 








                                                                                            if l1lll11l 														==														lII1lIll 																:																









                                                                                                                   Ill1llIl 										=										llI1Il1ll1I1l1I1IIll 






                                                                                            if l1lll11l 											==											I1ll11lI                       :                      



                                                                                                                   Ill1llIl                              =                             ll1IIIl1Il 





                                                                     if Ill1llIl 											==											ll1IIIl1Il 									:									





                                                                                            raise WORLD_GENERATOR_STATUS 												.												EMPTY_WORLD_NAME 										(										                               )                               





                                                                     if Ill1llIl                               ==                              llI1Il1ll1I1l1I1IIll                     :                    








                                                                                            pass 
                                                                     l11lll11                 :                l1l1ll11                       =                      													[													                 ]                 


                                                                     l111II1l 																:																Il1111Il1IlI1l 																=																conf_path                           (                          												)												                       +                       lI1IIllI 													.													format                         (                        lll11I1I 										)										





                                                                     Il1l111I 								=								llllIIll 
                                                                     Ill1IIII                                =                               l1llIIlI 





                                                                     if not I1I1I1lI 											(											I1lI1lI1l1lIllI 															)																							:								





                                                                                            Ill1IIII                         =                        I1IlIlll11IIl1lII 



                                                                     else                               :                              








                                                                                            Ill1IIII 											=											lI1lII1l 







                                                                     if Ill1IIII                          ==                         lIIII1III111 													:													
                                                                                            if not l1111ll1                         (                        IIl11I1l 														,														II11ll1IlI 													)													                          :                          

                                                                                                                   Ill1IIII 													=													lll1Il11 


                                                                                            else 									:									








                                                                                                                   Ill1IIII                           =                          I1IlIlll11IIl1lII 
                                                                     if Ill1IIII 													==													lll1Il11                                 :                                









                                                                                            Il1l111I                   =                  ll1IIIl1Il 




                                                                     if Ill1IIII 										==										I1IlIlll11IIl1lII                      :                     









                                                                                            Il1l111I                              =                             IllIIl1I 


                                                                     if Il1l111I 														==														ll1IIIl1Il 														:														

                                                                                            I1lI11l1 									=									Il11IllI 




                                                                                            if not IIIl1llllIl1I11Il                  :                 






                                                                                                                   I1lI11l1 													=													II11l1lI 


                                                                                            else 															:															
                                                                                                                   I1lI11l1                  =                 I1IlIlll11IIl1lII 






                                                                                            if I1lI11l1                      ==                     IIIlI1I1Il11                   :                  








                                                                                                                   if not os                         .                        path 														.														exists                   (                  l111II1l 												)												                      :                      

                                                                                                                                          I1lI11l1 											=											llI1I111 









                                                                                                                   else                           :                          




                                                                                                                                          I1lI11l1                   =                  II11l1lI 







                                                                                            if I1lI11l1 														==														II11l1lI                              :                             







                                                                                                                   Il1l111I 															=															IllIIl1I 




                                                                                            if I1lI11l1 											==											llI1I111                   :                  








                                                                                                                   Il1l111I                                =                               II11l1lI 



                                                                     if Il1l111I 										==										II11l1lI                              :                             

                                                                                            try                 :                




                                                                                                                   os 													.													makedirs 												(												l111II1l                          )                         







                                                                                            except OSError as e 										:										





                                                                                                                   l11111I1 											=											I1lll1lI 


                                                                                                                   II11I1I1 																=																I1l1l11I 


                                                                                                                   if not lIllI1II 														:														

                                                                                                                                          II11I1I1 																=																Il11IllI 






                                                                                                                   else                    :                   




                                                                                                                                          II11I1I1                     =                    lI1lIIll 







                                                                                                                   if II11I1I1                               ==                              lI1l11I1 										:										



                                                                                                                                          if not l1111ll1                         (                        e 															.															winerror                        ,                       II1l1lIl11l1II 												)												                       :                       




                                                                                                                                                                 II11I1I1 																=																l11l1l1l 

                                                                                                                                          else                  :                 





                                                                                                                                                                 II11I1I1 															=															Il11IllI 







                                                                                                                   if II11I1I1 												==												lIIIIlll                         :                        








                                                                                                                                          l11111I1 												=												lI11Il11 
                                                                                                                   if II11I1I1                                ==                               I11I11II                               :                              




                                                                                                                                          l11111I1 													=													Il11IllI 




                                                                                                                   if l11111I1                    ==                   II1IIl1l                     :                    
                                                                                                                                          l1111I11 											=											lI1Ill1l 






                                                                                                                                          if not llI1Il1ll1I1l1I1IIll                  :                 

                                                                                                                                                                 l1111I11                    =                   lll1Il11 








                                                                                                                                          else 												:												




                                                                                                                                                                 l1111I11                          =                         l1IllIl1 




                                                                                                                                          if l1111I11                   ==                  lll1Il11 								:								




                                                                                                                                                                 if not IlllI11l                          (                         ll1I1IlI                                 )                                										:										


                                                                                                                                                                                        l1111I11                      =                     l1IllIl1 



                                                                                                                                                                 else 								:								



                                                                                                                                                                                        l1111I11 														=														l11l1l1l 
                                                                                                                                          if l1111I11                           ==                          lIIIIlll 													:													





                                                                                                                                                                 l11111I1                    =                   lI11Il11 

                                                                                                                                          if l1111I11                    ==                   lll1lI1l 													:													








                                                                                                                                                                 l11111I1                           =                          l1III1l1 




                                                                                                                   if l11111I1 															==															l1III1l1 														:														









                                                                                                                                          raise WORLD_GENERATOR_STATUS 														.														OS_ERROR                    (                   															)															





                                                                                                                   if l11111I1                       ==                      llll1lIl 											:											

                                                                                                                                          raise WORLD_GENERATOR_STATUS 														.														INVALID_WORLD_NAME                      (                     								)								









                                                                                            l1lI1l11 													(													l111II1l                    +                   IlI11Ill                              ,                             lII11II1lllllI1lI                                )                               







                                                                     if Il1l111I                      ==                     Illll1lI                            :                           







                                                                                            pass 


                                                                     for llI1IllI in IlIl1lIl 								(								I111III1 													)																									:												
                                                                                            lIll1Il1                   =                  IIlI11II 
                                                                                            ll111Ill 													=													IlI1IIIlIlI1I11l1llI 

                                                                                            if not I1I1I1lI 								(								Illll1lI 								)																	:									
                                                                                                                   ll111Ill 										=										lIIl1III 




                                                                                            else                          :                         



                                                                                                                   ll111Ill 																=																Il1l111lIl 



                                                                                            if ll111Ill                      ==                     lIIl1III 												:												

                                                                                                                   if not I1I1I1lI                                (                               I1IIl11l 															)																										:											



                                                                                                                                          ll111Ill                            =                           lI11lIll 
                                                                                                                   else                             :                            




                                                                                                                                          ll111Ill                      =                     IllI11llII1 







                                                                                            if ll111Ill                         ==                        l11lI1Il 															:															









                                                                                                                   lIll1Il1 								=								Il1IlIll 
                                                                                            if ll111Ill 															==															llll1lIl                               :                              



                                                                                                                   lIll1Il1 										=										I1l1l11I 
                                                                                            if lIll1Il1                            ==                           II1I1Il1                   :                  

                                                                                                                   I1Il1I1l                 =                I1l111I1 








                                                                                                                   if not IlllI11l                              (                             lI11ll1lII1l                          )                                              :                     

                                                                                                                                          I1Il1I1l                    =                   lIIIlllI 
                                                                                                                   else 															:															
                                                                                                                                          I1Il1I1l                     =                    IlI1IIIlIlI1I11l1llI 









                                                                                                                   if I1Il1I1l                         ==                        lIlI11lI                  :                 


                                                                                                                                          lIlIl1l1                                 =                                Il1Il1IIlII11II1I 

                                                                                                                                          Il1llIl1 										=										lIIl1III 
                                                                                                                                          I1lI1l111I1l                                =                               Ill1111I 









                                                                                                                                          if not I1I1I1lI                                (                               II11ll1IlI 											)											                         :                         









                                                                                                                                                                 I1lI1l111I1l 								=								l11lIIl1 







                                                                                                                                          else 													:													


                                                                                                                                                                 I1lI1l111I1l 																=																IIlll1II 








                                                                                                                                          if I1lI1l111I1l                                 ==                                l11lIIl1                            :                           



                                                                                                                                                                 if not I1I1I1lI                          (                         IIlIIIIl                         )                        										:										







                                                                                                                                                                                        I1lI1l111I1l 								=								IlIl1III 


                                                                                                                                                                 else 								:								








                                                                                                                                                                                        I1lI1l111I1l                     =                    IlllI1II 







                                                                                                                                          if I1lI1l111I1l                   ==                  IlIl1III 													:													









                                                                                                                                                                 Il1llIl1 														=														Il1llIl11I1IIl1 




                                                                                                                                          if I1lI1l111I1l 																==																Illll1Il 													:													


                                                                                                                                                                 Il1llIl1                   =                  IIIlI1I1Il11 


                                                                                                                                          if Il1llIl1                 ==                llIl1I1l 												:												




                                                                                                                                                                 IlI1Il1l                                 =                                III1lIlI1llI1l 






                                                                                                                                                                 if lIlllIIl                  (                 Illl1Il1 											,											ll11l11l                               )                                              :                






                                                                                                                                                                                        IlI1Il1l                      =                     llI1111I 



                                                                                                                                                                 else 											:											



                                                                                                                                                                                        IlI1Il1l                               =                              Il11l1ll 



                                                                                                                                                                 if IlI1Il1l                    ==                   IIl111l1 													:													
                                                                                                                                                                                        if l1111ll1                     (                    lIlI11lI                  ,                 lI1l11ll                        )                       															:															




                                                                                                                                                                                                               IlI1Il1l 								=								llI1111I 





                                                                                                                                                                                        else 											:											
                                                                                                                                                                                                               IlI1Il1l                 =                I1IIl1Il 






                                                                                                                                                                 if IlI1Il1l                               ==                              llI1lII1                         :                        
                                                                                                                                                                                        Il1llIl1                                 =                                I1lI1lI1l1lIllI 







                                                                                                                                                                 if IlI1Il1l 								==								lIIlIIII                          :                         




                                                                                                                                                                                        Il1llIl1                       =                      I1IlIlll11IIl1lII 




                                                                                                                                          if Il1llIl1                 ==                I1Ill1 															:															






                                                                                                                                                                 lIlIl1l1 									=									IIIl1ll1 


                                                                                                                                          if Il1llIl1                            ==                           IIllIll1 														:														









                                                                                                                                                                 lIlIl1l1 													=													IIIll11ll1lIl1I11 







                                                                                                                                          if lIlIl1l1                   ==                  lIIlllI1                    :                   



                                                                                                                                                                 ll111l11                    =                   I1l111I1 
                                                                                                                                                                 IIl1l1I1I                           =                          l1ll11Il 

                                                                                                                                                                 if not lll1Il11 											:											
                                                                                                                                                                                        IIl1l1I1I 													=													Ill1111I 


                                                                                                                                                                 else                     :                    
                                                                                                                                                                                        IIl1l1I1I                  =                 I1lI1l11 








                                                                                                                                                                 if IIl1l1I1I 															==															l1I1I11l 									:									









                                                                                                                                                                                        if lI1lI1Il11II1I 												(												lI1llIl1                        ,                       lll1Il11 															)																															:																


                                                                                                                                                                                                               IIl1l1I1I                                =                               IIlIIIIl 
                                                                                                                                                                                        else                       :                      


                                                                                                                                                                                                               IIl1l1I1I 														=														IIlIll1l 







                                                                                                                                                                 if IIl1l1I1I 														==														l1lllIll                              :                             





                                                                                                                                                                                        ll111l11                                =                               I1lII1lI 


                                                                                                                                                                 if IIl1l1I1I 												==												ll11l1I1ll1III1 																:																




                                                                                                                                                                                        ll111l11 											=											llI1Il1ll1I1l1I1IIll 







                                                                                                                                                                 if ll111l11 														==														llI1Il1ll1I1l1I1IIll                      :                     


                                                                                                                                                                                        ll11ll11                             =                            llIIl11I 







                                                                                                                                                                                        if not lI1lI1l1lI1l1lll1II 											.											lIIlIl11 														(														lI1Ill1l 																)																												:												





                                                                                                                                                                                                               ll11ll11 								=								IlII1l1l 
                                                                                                                                                                                        else                                 :                                







                                                                                                                                                                                                               ll11ll11                               =                              I1IlI1l1 





                                                                                                                                                                                        if ll11ll11 								==								l1lIIl11 											:											

                                                                                                                                                                                                               if not lI1lI1l1lI1l1lll1II                 .                lIIlIl11                    (                   lll1Il11                  )                 									:									








                                                                                                                                                                                                                                      ll11ll11                 =                l1lllIll 





                                                                                                                                                                                                               else                         :                        





                                                                                                                                                                                                                                      ll11ll11 															=															llll1111 








                                                                                                                                                                                        if ll11ll11 															==															lIllllI11lIIl1l1lI 								:								





                                                                                                                                                                                                               ll111l11                      =                     lllII1Il 
                                                                                                                                                                                        if ll11ll11                  ==                 l1lllIll                    :                   




                                                                                                                                                                                                               ll111l11 									=									llllIIll 




                                                                                                                                                                 if ll111l11 																==																lIIl1IIl 																:																





                                                                                                                                                                                        lIlIl1l1                           =                          lIlI11lI 



                                                                                                                                                                 if ll111l11 															==															l11lI11I                           :                          

                                                                                                                                                                                        lIlIl1l1                          =                         ll11l1I1ll1III1 








                                                                                                                                          if lIlIl1l1 												==												Il1l1ll1 									:									






                                                                                                                                                                 I1Il1I1l                                 =                                I111l1ll 
                                                                                                                                          if lIlIl1l1 														==														I111l1ll                              :                             
                                                                                                                                                                 I1Il1I1l                             =                            lIIIlllI 





                                                                                                                   if I1Il1I1l 									==									IIIll11ll1lIl1I11                                 :                                






                                                                                                                                          lIll1Il1                                 =                                lIIlllI1 









                                                                                                                   if I1Il1I1l 														==														IlI11ll1II 								:								



                                                                                                                                          lIll1Il1 										=										Il1IlIll 

                                                                                            if lIll1Il1 														==														I1Il1lll 											:											


                                                                                                                   pass 





                                                                                            if lIll1Il1 									==									lI1I1l11Ill 													:													







                                                                                                                   Illl1lI1 									=									l11lIl1I                                 (                                I111III1 											,											IllIIl1I 											)											







                                                                                                                   Il11l1111IIllI1llll                      .                     progression                     +=                    I111III1                             *                            lIll1I11 										/										Illl1lI1 
                                                                                                                   for lIII1lII in Il1llllI 									(									llII111l                 ,                I1lIlIIl 											)																										:															


                                                                                                                                          if 										(										not IlllI11l 															(															I1ll11lI                          )                         or I1lI1l11 															)															and                             (                            lI1lI1l1lI1l1lll1II                          .                         lIIlIl11                    (                   lI1III1l                    )                   and IlllI11l 													(													l1Il1III 															)																								)									or                  (                                            (                           llll1111                         <=                        l1llIIlI or lIl11111                                 !=                                lI1Ill1l1Il1l1I 											)											or                            (                           ll1III                      >=                     lIllIIII or not I1I1I1lI 										(										I111lII1 									)									                              )                                              )                                 :                 




                                                                                                                                                                 for lI1l11 in lII1I11l                                (                               lI1IlIll                                 ,                                II11ll1IlI 											)																					:										






                                                                                                                                                                                        for Il11IIIl in IlIl1lIl 													(													I111III1 										)																							:													



                                                                                                                                                                                                               lIlII1Il                  =                 I1l1l11I 







                                                                                                                                                                                                               IlIIll11 												=												l1lllIll 





                                                                                                                                                                                                               if lI1lI1Il11II1I 											(											IlIIllIlI11 										,										II1I1l1l                              )                             											:											









                                                                                                                                                                                                                                      IlIIll11 													=													I1llllIlIIl1II 





                                                                                                                                                                                                               else                             :                            


                                                                                                                                                                                                                                      IlIIll11                     =                    lI111Il1l1 






                                                                                                                                                                                                               if IlIIll11                    ==                   I1lllIll                             :                            



                                                                                                                                                                                                                                      if not I1I1I1lI 														(														I1l11ll1 																)																                      :                      








                                                                                                                                                                                                                                                             IlIIll11                 =                II1I1lll 

                                                                                                                                                                                                                                      else                                 :                                


                                                                                                                                                                                                                                                             IlIIll11                             =                            I1Il1lII 






                                                                                                                                                                                                               if IlIIll11 													==													ll1IIIl1Il 								:								






                                                                                                                                                                                                                                      lIlII1Il 											=											l1IIlIl1 




                                                                                                                                                                                                               if IlIIll11                 ==                Il1lIl11 											:											
                                                                                                                                                                                                                                      lIlII1Il                          =                         I111l1ll 


                                                                                                                                                                                                               if lIlII1Il                             ==                            Ill1I11 									:									




                                                                                                                                                                                                                                      llIll1ll                    =                   I11111l1 

                                                                                                                                                                                                                                      I1lIIll111Il                              =                             I1I1II1I 
                                                                                                                                                                                                                                      IIIll11I                          =                         l11lIIl1 







                                                                                                                                                                                                                                      IIl1IllI 								=								I1lllIll 









                                                                                                                                                                                                                                      if l1111ll1                            (                           IIl11I1l 									,									IIl11I1l 									)																			:										



                                                                                                                                                                                                                                                             IIl1IllI 															=															lI1lII1l 
                                                                                                                                                                                                                                      else                              :                             









                                                                                                                                                                                                                                                             IIl1IllI                          =                         lIIlI1I1 



                                                                                                                                                                                                                                      if IIl1IllI                              ==                             lll1II1I 										:										

                                                                                                                                                                                                                                                             if not IIIl1Il1 															:															


                                                                                                                                                                                                                                                                                    IIl1IllI                                =                               I111lII1 


                                                                                                                                                                                                                                                             else 											:											









                                                                                                                                                                                                                                                                                    IIl1IllI                     =                    l1IlIl1I 









                                                                                                                                                                                                                                      if IIl1IllI                   ==                  lI1lII1l 										:										


                                                                                                                                                                                                                                                             IIIll11I 														=														lIIl1III 









                                                                                                                                                                                                                                      if IIl1IllI                           ==                          I1lIl1lI                             :                            



                                                                                                                                                                                                                                                             IIIll11I                           =                          IlI1Il11 









                                                                                                                                                                                                                                      if IIIll11I 																==																IlI1Il11                 :                




                                                                                                                                                                                                                                                             lI1I1I1I 																=																l11lI11I 


                                                                                                                                                                                                                                                             if not lI1lI1l1lI1l1lll1II 												.												lIIlIl11 									(									I1lI1lI1l1lIllI                   )                  									:									



                                                                                                                                                                                                                                                                                    lI1I1I1I 													=													I1lI1l11 





                                                                                                                                                                                                                                                             else 															:															




                                                                                                                                                                                                                                                                                    lI1I1I1I                             =                            lIIl1III 



                                                                                                                                                                                                                                                             if lI1I1I1I                      ==                     IIlI1IlI 									:									

                                                                                                                                                                                                                                                                                    if not II1llIlI11ll1I                      :                     






                                                                                                                                                                                                                                                                                                           lI1I1I1I 										=										lll1lI1l 





                                                                                                                                                                                                                                                                                    else                     :                    








                                                                                                                                                                                                                                                                                                           lI1I1I1I 															=															llIl1Ill 






                                                                                                                                                                                                                                                             if lI1I1I1I 											==											IIIlIl1lIl1lll1l1I1l                     :                    



                                                                                                                                                                                                                                                                                    IIIll11I                            =                           lll111II 
                                                                                                                                                                                                                                                             if lI1I1I1I                            ==                           lll1lI1l                          :                         







                                                                                                                                                                                                                                                                                    IIIll11I 											=											l1I1I1lI 





                                                                                                                                                                                                                                      if IIIll11I                        ==                       l11I1llI                                :                               




                                                                                                                                                                                                                                                             I1lIIll111Il 									=									IlI1Il11 
                                                                                                                                                                                                                                      if IIIll11I                         ==                        IIll11lI                    :                   








                                                                                                                                                                                                                                                             I1lIIll111Il 									=									lI111Il1l1 

                                                                                                                                                                                                                                      if I1lIIll111Il 																==																I1lllIll                             :                            









                                                                                                                                                                                                                                                             IIl1IlI11I1I1                      =                     I1I111IlI111I1lll 







                                                                                                                                                                                                                                                             llll1III                         =                        IllIIl1I 







                                                                                                                                                                                                                                                             if not ll1l1lll                 :                








                                                                                                                                                                                                                                                                                    llll1III                                =                               l1l1l1ll 








                                                                                                                                                                                                                                                             else 										:										


                                                                                                                                                                                                                                                                                    llll1III 											=											lll1lI1l 




                                                                                                                                                                                                                                                             if llll1III 								==								lll111II 											:											








                                                                                                                                                                                                                                                                                    if l1111ll1                                 (                                II11ll1IlI                                 ,                                II1l1II1                     )                                           :                       







                                                                                                                                                                                                                                                                                                           llll1III 									=									l1ll11Il 





                                                                                                                                                                                                                                                                                    else                                :                               



                                                                                                                                                                                                                                                                                                           llll1III                           =                          Il1ll1l1 
                                                                                                                                                                                                                                                             if llll1III                     ==                    l1ll11Il                   :                  
                                                                                                                                                                                                                                                                                    IIl1IlI11I1I1                  =                 IlllI1I1 







                                                                                                                                                                                                                                                             if llll1III                      ==                     lI1IlI1I                                :                               








                                                                                                                                                                                                                                                                                    IIl1IlI11I1I1 													=													I1IIl1Il 








                                                                                                                                                                                                                                                             if IIl1IlI11I1I1                          ==                         II11ll1IlI                      :                     

                                                                                                                                                                                                                                                                                    lIIllIII 													=													ll11lIll 





                                                                                                                                                                                                                                                                                    if l1111ll1 									(									IIlIllI1 															,															llll1II1                               )                              																:																

                                                                                                                                                                                                                                                                                                           lIIllIII                      =                     ll1l1111 







                                                                                                                                                                                                                                                                                    else 								:								

                                                                                                                                                                                                                                                                                                           lIIllIII                                =                               l11lI1II 
                                                                                                                                                                                                                                                                                    if lIIllIII                               ==                              lI1lIIll                              :                             









                                                                                                                                                                                                                                                                                                           if not I1I1I1lI 								(								lIIIIlll 											)											                :                

                                                                                                                                                                                                                                                                                                                                  lIIllIII 										=										I1I11111 




                                                                                                                                                                                                                                                                                                           else                  :                 







                                                                                                                                                                                                                                                                                                                                  lIIllIII                              =                             Illll1lI 






                                                                                                                                                                                                                                                                                    if lIIllIII 												==												IIII1l1I                        :                       






                                                                                                                                                                                                                                                                                                           IIl1IlI11I1I1 											=											I1IIl1Il 




                                                                                                                                                                                                                                                                                    if lIIllIII                               ==                              IlllI1Il                                 :                                


                                                                                                                                                                                                                                                                                                           IIl1IlI11I1I1                   =                  lIl11111 




                                                                                                                                                                                                                                                             if IIl1IlI11I1I1 									==									lIl11111                               :                              







                                                                                                                                                                                                                                                                                    I1lIIll111Il 									=									IlI1Il11 
                                                                                                                                                                                                                                                             if IIl1IlI11I1I1 												==												I1IIl1Il 								:								









                                                                                                                                                                                                                                                                                    I1lIIll111Il 														=														l1lllI1I 





                                                                                                                                                                                                                                      if I1lIIll111Il                           ==                          I1111l1l                             :                            
                                                                                                                                                                                                                                                             llIll1ll 														=														I1l1Il1l1lIl1IIl 








                                                                                                                                                                                                                                      if I1lIIll111Il 																==																IlI1Il11                             :                            


                                                                                                                                                                                                                                                             llIll1ll 													=													lI1I1l11Ill 

                                                                                                                                                                                                                                      if llIll1ll                                 ==                                lI1I1l11Ill 															:															









                                                                                                                                                                                                                                                             if not lI1lI1l1lI1l1lll1II 																.																lIIlIl11                              (                             I111lII1 															)															                    :                    






                                                                                                                                                                                                                                                                                    llIll1ll 																=																I1l1Il1l1lIl1IIl 





                                                                                                                                                                                                                                                             else                              :                             
                                                                                                                                                                                                                                                                                    llIll1ll                              =                             ll1111lll11Il1l1 



                                                                                                                                                                                                                                      if llIll1ll 											==											lIl1l1Il                  :                 






                                                                                                                                                                                                                                                             lIlII1Il 											=											I111l1ll 






                                                                                                                                                                                                                                      if llIll1ll                             ==                            Il1ll11I                  :                 

                                                                                                                                                                                                                                                             lIlII1Il                   =                  lIIlllI1 








                                                                                                                                                                                                               if lIlII1Il 													==													I1Il1lll                               :                              








                                                                                                                                                                                                                                      pass 

                                                                                                                                                                                                               if lIlII1Il                             ==                            IIIIIlIl 								:								

                                                                                                                                                                                                                                      l11lll1I 												=												llIllI1l 														(														I1l1l11l 												(																											[															Il11IIIl 									/									I111III1                         ,                        llI1IllI                           /                          I111III1                    ]                                    )                 													*													llI1Il1ll1I1l1I1IIll 												)												



                                                                                                                                                                                                                                      IllIIIII11l111 									=									lll1Il11 





                                                                                                                                                                                                                                      lI1l11II                              =                             lIl11111 





                                                                                                                                                                                                                                      if not lI1lI1l1lI1l1lll1II                        .                       lIIlIl11 											(											I1I1II1I                           )                          									:									




                                                                                                                                                                                                                                                             lI1l11II 										=										I1l1Il1l1lIl1IIl 



                                                                                                                                                                                                                                      else                          :                         

                                                                                                                                                                                                                                                             lI1l11II                                =                               IIIl1l1I 



                                                                                                                                                                                                                                      if lI1l11II                            ==                           l1lllI1I                 :                


                                                                                                                                                                                                                                                             if not lIlllIIl                        (                       I11IIllI 												,												lI1l1Ill 												)																							:											




                                                                                                                                                                                                                                                                                    lI1l11II                         =                        ll11l11l 







                                                                                                                                                                                                                                                             else                                :                               



                                                                                                                                                                                                                                                                                    lI1l11II                           =                          lll1Il11 
                                                                                                                                                                                                                                      if lI1l11II                       ==                      lll1Il11                             :                            






                                                                                                                                                                                                                                                             IllIIIII11l111                   =                  lIl11111 



                                                                                                                                                                                                                                      if lI1l11II                 ==                I1l1Il1l1lIl1IIl 														:														





                                                                                                                                                                                                                                                             IllIIIII11l111                       =                      IIlI1lI1 
                                                                                                                                                                                                                                      if IllIIIII11l111                         ==                        lI1Ill1l1Il1l1I                             :                            





                                                                                                                                                                                                                                                             I1111llI 												=												IlIII1II 



                                                                                                                                                                                                                                                             if not l1111ll1                         (                        IIlIlIl1 												,												ll1IIIl1Il                   )                  											:											
                                                                                                                                                                                                                                                                                    I1111llI 											=											IIl111l1 

                                                                                                                                                                                                                                                             else 											:											



                                                                                                                                                                                                                                                                                    I1111llI                            =                           IIl11I1l 


                                                                                                                                                                                                                                                             if I1111llI 																==																I11I1I1111lIlI1lII1 											:											






                                                                                                                                                                                                                                                                                    if not l11II1l1 														(														random                 .                random                       (                      								)																		,										II1lll1l 										)																		:								




                                                                                                                                                                                                                                                                                                           I1111llI 														=														llI1I111 




                                                                                                                                                                                                                                                                                    else                      :                     







                                                                                                                                                                                                                                                                                                           I1111llI                     =                    I111I1II 








                                                                                                                                                                                                                                                             if I1111llI 								==								I1IlIll1                               :                              



                                                                                                                                                                                                                                                                                    IllIIIII11l111 																=																I1l1llIl 







                                                                                                                                                                                                                                                             if I1111llI 												==												lI111I1lllI                       :                      


                                                                                                                                                                                                                                                                                    IllIIIII11l111 								=								l1lII1l1 







                                                                                                                                                                                                                                      if IllIIIII11l111                    ==                   l1lII1l1                              :                             
                                                                                                                                                                                                                                                             pass 


                                                                                                                                                                                                                                      if IllIIIII11l111                           ==                          IIlI1lI1                             :                            




                                                                                                                                                                                                                                                             l11lll1I 															+=															random                      .                     randint                              (                             											-											lI1llIl1                        ,                       IlIllIIlI1 													)													






                                                                                                                                                                                                                                      llll1lII 															=															lIIlI1I1 




                                                                                                                                                                                                                                      Ill1I111                              =                             II1llIlI11ll1I 


                                                                                                                                                                                                                                      if l11II1l1                        (                       random                      .                     random                 (                																)																															,															lIIIl11I                           )                          													:													


                                                                                                                                                                                                                                                             Ill1I111                 =                I1Il1lII 


                                                                                                                                                                                                                                      else 																:																



                                                                                                                                                                                                                                                             Ill1I111 									=									Illll1Il 




                                                                                                                                                                                                                                      if Ill1I111                        ==                       Ill1II1I1l1II1                             :                            









                                                                                                                                                                                                                                                             if not lI1lI1l1lI1l1lll1II                            .                           lIIlIl11                               (                              I1lIl1lI 														)														                      :                      






                                                                                                                                                                                                                                                                                    Ill1I111 															=															I1ll1ll1 







                                                                                                                                                                                                                                                             else                    :                   









                                                                                                                                                                                                                                                                                    Ill1I111 										=										IlllI1Il 





                                                                                                                                                                                                                                      if Ill1I111 															==															IIIl1llllIl1I11Il                 :                







                                                                                                                                                                                                                                                             llll1lII 									=									II1I1lll 








                                                                                                                                                                                                                                      if Ill1I111                       ==                      l1lIIl11 																:																





                                                                                                                                                                                                                                                             llll1lII 															=															lIll11l1 








                                                                                                                                                                                                                                      if llll1lII                   ==                  lIll11l1 														:														



                                                                                                                                                                                                                                                             I1III1I1                             =                            I1ll1I1l 



                                                                                                                                                                                                                                                             if not lIll11l1                          :                         




                                                                                                                                                                                                                                                                                    I1III1I1 														=														I11IlllI 






                                                                                                                                                                                                                                                             else 													:													








                                                                                                                                                                                                                                                                                    I1III1I1 										=										ll1II1I1 







                                                                                                                                                                                                                                                             if I1III1I1 														==														IIllIIl1 								:								







                                                                                                                                                                                                                                                                                    if l11II1l1                              (                             Illll1Il                  ,                 I1l111I1                       )                                                   :                             







                                                                                                                                                                                                                                                                                                           I1III1I1 														=														IlI1II1I 

                                                                                                                                                                                                                                                                                    else                              :                             
                                                                                                                                                                                                                                                                                                           I1III1I1                            =                           lI111l11 









                                                                                                                                                                                                                                                             if I1III1I1 											==											I11IlllI                    :                   








                                                                                                                                                                                                                                                                                    llll1lII 																=																Il1lIl11 







                                                                                                                                                                                                                                                             if I1III1I1 										==										lI111l11 									:									








                                                                                                                                                                                                                                                                                    llll1lII 								=								I1lI1I1l1lI1l1IlI 
                                                                                                                                                                                                                                      if llll1lII                                 ==                                II1l1II1 													:													





                                                                                                                                                                                                                                                             pass 






                                                                                                                                                                                                                                      if llll1lII                        ==                       I1Ill1                               :                              






                                                                                                                                                                                                                                                             II1lllIl 																=																II11l1lI 




                                                                                                                                                                                                                                                             II1llIIl 																=																llII111l 




                                                                                                                                                                                                                                                             if not l1lIIlII 														:														






                                                                                                                                                                                                                                                                                    II1llIIl 													=													I11l1I1l 





                                                                                                                                                                                                                                                             else 								:								




                                                                                                                                                                                                                                                                                    II1llIIl 										=										llI1111I 




                                                                                                                                                                                                                                                             if II1llIIl                         ==                        l1lIIl11 													:													







                                                                                                                                                                                                                                                                                    if not ll1III 											:											








                                                                                                                                                                                                                                                                                                           II1llIIl 									=									lIIlIIII 






                                                                                                                                                                                                                                                                                    else 										:										




                                                                                                                                                                                                                                                                                                           II1llIIl                  =                 l11I1lIl 

                                                                                                                                                                                                                                                             if II1llIIl 													==													I11ll111II 												:												









                                                                                                                                                                                                                                                                                    II1lllIl 											=											l1lIIlII 



                                                                                                                                                                                                                                                             if II1llIIl                 ==                l1lll1I1 												:												
                                                                                                                                                                                                                                                                                    II1lllIl                               =                              I11Il1 








                                                                                                                                                                                                                                                             if II1lllIl 									==									IIlIlIl1                         :                        






                                                                                                                                                                                                                                                                                    II1IllI                            =                           l1II11Il 





                                                                                                                                                                                                                                                                                    if not lI1lI1l1lI1l1lll1II 								.								lIIlIl11 													(													I11l1I1l                       )                      										:										

                                                                                                                                                                                                                                                                                                           II1IllI                     =                    llIl1Ill 



                                                                                                                                                                                                                                                                                    else 														:														




                                                                                                                                                                                                                                                                                                           II1IllI                          =                         I1l1llIl 









                                                                                                                                                                                                                                                                                    if II1IllI 								==								I1l1llIl 														:														
                                                                                                                                                                                                                                                                                                           if not l11II1l1                 (                random                   .                  random                   (                  								)																						,														IlI1l1l1 												)												                      :                      



                                                                                                                                                                                                                                                                                                                                  II1IllI 														=														lllI1lll 






                                                                                                                                                                                                                                                                                                           else 																:																






                                                                                                                                                                                                                                                                                                                                  II1IllI 											=											lllII1Il 






                                                                                                                                                                                                                                                                                    if II1IllI 										==										Ill1I1I1                               :                              






                                                                                                                                                                                                                                                                                                           II1lllIl                    =                   I1lI1I1l1Ill1 






                                                                                                                                                                                                                                                                                    if II1IllI                              ==                             I1lII1lI 												:												





                                                                                                                                                                                                                                                                                                           II1lllIl                       =                      llI1111I 






                                                                                                                                                                                                                                                             if II1lllIl                           ==                          I1lI1I1l1Ill1                    :                   





                                                                                                                                                                                                                                                                                    l11lll1I 													=													IIlI111l 








                                                                                                                                                                                                                                                             if II1lllIl 									==									lIIlIIII                              :                             







                                                                                                                                                                                                                                                                                    l11lll1I                             =                            random                                .                               randint 																(																Ill1111I                    ,                   I11IlllI 															)															






                                                                                                                                                                                                                                      for l1llllIl in 														[														Il1IlIll                        ]                                       :                







                                                                                                                                                                                                                                                             for lIlIII11 in lIIlI1IIIIIII1                     (                    l11lll1I                                 )                                									:									



                                                                                                                                                                                                                                                                                    lIllI1l11l 											=											I1lIlIIl 





                                                                                                                                                                                                                                                                                    IlII1IlI                            =                           llll1lIl 


                                                                                                                                                                                                                                                                                    lIlI1IlI1IIll 											=											II11Ill1l 




                                                                                                                                                                                                                                                                                    lI1I1111 												=												Il1l111lIl 






                                                                                                                                                                                                                                                                                    III1I11I 													=													lII1lI1l 




                                                                                                                                                                                                                                                                                    if not IlllI11l 								(								l1lllI1I 										)																										:																





                                                                                                                                                                                                                                                                                                           III1I11I                        =                       II1I1lll 


                                                                                                                                                                                                                                                                                    else                              :                             



                                                                                                                                                                                                                                                                                                           III1I11I                              =                             IIl111l1 








                                                                                                                                                                                                                                                                                    if III1I11I 											==											I1I1II1I 										:										




                                                                                                                                                                                                                                                                                                           if not l1IllIl1                       :                      





                                                                                                                                                                                                                                                                                                                                  III1I11I 															=															II1l1II1 

                                                                                                                                                                                                                                                                                                           else 																:																






                                                                                                                                                                                                                                                                                                                                  III1I11I                             =                            I1Il1lII 









                                                                                                                                                                                                                                                                                    if III1I11I                               ==                              Il1lIl11 																:																

                                                                                                                                                                                                                                                                                                           lI1I1111 								=								l1III1l1 






                                                                                                                                                                                                                                                                                    if III1I11I                   ==                  lII1IIII 											:											





                                                                                                                                                                                                                                                                                                           lI1I1111                   =                  I1Ill1 
                                                                                                                                                                                                                                                                                    if lI1I1111                      ==                     l1llIIlI 																:																



                                                                                                                                                                                                                                                                                                           II11I1ll 											=											IIIl1l1I 
                                                                                                                                                                                                                                                                                                           if not lI1Il11I                         (                        lIIII1III111                        ,                       I1I1II1I                  )                                           :                          






                                                                                                                                                                                                                                                                                                                                  II11I1ll 														=														IIIlI11lllIl 

                                                                                                                                                                                                                                                                                                           else 														:														








                                                                                                                                                                                                                                                                                                                                  II11I1ll                          =                         I11Il1 







                                                                                                                                                                                                                                                                                                           if II11I1ll                               ==                              IIIlI11lllIl 										:										
                                                                                                                                                                                                                                                                                                                                  if not l1111ll1 									(									I11l1I1l 															,															Illll1Il 										)										                          :                          

                                                                                                                                                                                                                                                                                                                                                         II11I1ll                          =                         I1ll11lI 


                                                                                                                                                                                                                                                                                                                                  else 								:								







                                                                                                                                                                                                                                                                                                                                                         II11I1ll 										=										I11Il1 







                                                                                                                                                                                                                                                                                                           if II11I1ll 												==												IIlIlIl1                  :                 









                                                                                                                                                                                                                                                                                                                                  lI1I1111 																=																IIIlI1I1Il11 
                                                                                                                                                                                                                                                                                                           if II11I1ll 																==																II1I1Il1 												:												








                                                                                                                                                                                                                                                                                                                                  lI1I1111 													=													l11lII1I 

                                                                                                                                                                                                                                                                                    if lI1I1111 								==								IIIlI1I1Il11 														:														





                                                                                                                                                                                                                                                                                                           lIlI1IlI1IIll 											=											IIIl1l1I 









                                                                                                                                                                                                                                                                                    if lI1I1111                    ==                   lIlI1II1I11I11l 										:										







                                                                                                                                                                                                                                                                                                           lIlI1IlI1IIll 								=								l1lIIlII 
                                                                                                                                                                                                                                                                                    if lIlI1IlI1IIll                     ==                    l1lllI1I                    :                   

                                                                                                                                                                                                                                                                                                           l1I1IIIllII 								=								lI1l11I1 








                                                                                                                                                                                                                                                                                                           IIlIllIIII11lII1                      =                     I11I11l1 





                                                                                                                                                                                                                                                                                                           if not l1IIll1I                        :                       









                                                                                                                                                                                                                                                                                                                                  IIlIllIIII11lII1                   =                  lllI1lll 



                                                                                                                                                                                                                                                                                                           else 												:												

                                                                                                                                                                                                                                                                                                                                  IIlIllIIII11lII1                  =                 II11I11I 




                                                                                                                                                                                                                                                                                                           if IIlIllIIII11lII1                          ==                         I1IIl1Il 													:													








                                                                                                                                                                                                                                                                                                                                  if not IIIllIl1 													:													





                                                                                                                                                                                                                                                                                                                                                         IIlIllIIII11lII1 								=								l11lI1II 


                                                                                                                                                                                                                                                                                                                                  else 								:								
                                                                                                                                                                                                                                                                                                                                                         IIlIllIIII11lII1                 =                lIlI111lII1II1ll 


                                                                                                                                                                                                                                                                                                           if IIlIllIIII11lII1                             ==                            l11lI1II                  :                 


                                                                                                                                                                                                                                                                                                                                  l1I1IIIllII                         =                        Il11l1Il 







                                                                                                                                                                                                                                                                                                           if IIlIllIIII11lII1 															==															lIlI111lII1II1ll                         :                        
                                                                                                                                                                                                                                                                                                                                  l1I1IIIllII 													=													IIIl1Il1 


                                                                                                                                                                                                                                                                                                           if l1I1IIIllII                    ==                   II1lll1I 									:									





                                                                                                                                                                                                                                                                                                                                  I1lIlIll 								=								lI1IlIll 









                                                                                                                                                                                                                                                                                                                                  if not lI1lI1l1lI1l1lll1II                      .                     lIIlIl11 										(										IIlll1II 								)								                            :                            


                                                                                                                                                                                                                                                                                                                                                         I1lIlIll                              =                             lIl11111 







                                                                                                                                                                                                                                                                                                                                  else 														:														


                                                                                                                                                                                                                                                                                                                                                         I1lIlIll                   =                  lI11IlII 


                                                                                                                                                                                                                                                                                                                                  if I1lIlIll                     ==                    I1lllllI 												:												









                                                                                                                                                                                                                                                                                                                                                         if not I1I1I1lI 																(																l1II1lII                         )                                            :                    






                                                                                                                                                                                                                                                                                                                                                                                I1lIlIll                  =                 lI11IlII 



                                                                                                                                                                                                                                                                                                                                                         else                           :                          


                                                                                                                                                                                                                                                                                                                                                                                I1lIlIll                            =                           I1l1llIl 

                                                                                                                                                                                                                                                                                                                                  if I1lIlIll                           ==                          lI1IlI1I                        :                       


                                                                                                                                                                                                                                                                                                                                                         l1I1IIIllII 														=														I1IIl1Il 



                                                                                                                                                                                                                                                                                                                                  if I1lIlIll                   ==                  lllI11I1 														:														

                                                                                                                                                                                                                                                                                                                                                         l1I1IIIllII 													=													IIIl1Il1 


                                                                                                                                                                                                                                                                                                           if l1I1IIIllII 										==										II11I11I                              :                             

                                                                                                                                                                                                                                                                                                                                  lIlI1IlI1IIll 												=												l11lI1II 


                                                                                                                                                                                                                                                                                                           if l1I1IIIllII                    ==                   lI1IlI1I                      :                     





                                                                                                                                                                                                                                                                                                                                  lIlI1IlI1IIll 													=													l1lIIlII 




                                                                                                                                                                                                                                                                                    if lIlI1IlI1IIll                             ==                            lI1lIIll                      :                     




                                                                                                                                                                                                                                                                                                           IlII1IlI 														=														II11ll1IlI 





                                                                                                                                                                                                                                                                                    if lIlI1IlI1IIll                                ==                               I1lI1I1l1Ill1                          :                         






                                                                                                                                                                                                                                                                                                           IlII1IlI 																=																I1lI11ll 
                                                                                                                                                                                                                                                                                    if IlII1IlI 													==													IIl11I1l                    :                   



                                                                                                                                                                                                                                                                                                           if not lI1lI1Il11II1I                             (                            lI1l11l1                                ,                               Il1I11l1 								)								                              :                              






                                                                                                                                                                                                                                                                                                                                  IlII1IlI 											=											I1Il1lII 
                                                                                                                                                                                                                                                                                                           else 															:															







                                                                                                                                                                                                                                                                                                                                  IlII1IlI                 =                l1I1I1II 

                                                                                                                                                                                                                                                                                    if IlII1IlI                    ==                   IIllIIl1                       :                      
                                                                                                                                                                                                                                                                                                           lIllI1l11l 													=													lll111II 





                                                                                                                                                                                                                                                                                    if IlII1IlI 															==															I1lI11ll                   :                  




                                                                                                                                                                                                                                                                                                           lIllI1l11l                          =                         II11l1lI 


                                                                                                                                                                                                                                                                                    if lIllI1l11l 												==												lIIl1III                        :                       







                                                                                                                                                                                                                                                                                                           lI111l1l 														=														I1lI1I1l1Ill1 



                                                                                                                                                                                                                                                                                                           if not l1I1l1l1 													:													


                                                                                                                                                                                                                                                                                                                                  lI111l1l 											=											II11I11I 






                                                                                                                                                                                                                                                                                                           else                            :                           





                                                                                                                                                                                                                                                                                                                                  lI111l1l 										=										IIIlI1I1Il11 







                                                                                                                                                                                                                                                                                                           if lI111l1l 												==												II11I11I                               :                              




                                                                                                                                                                                                                                                                                                                                  if not IlI1Il11 									:									



                                                                                                                                                                                                                                                                                                                                                         lI111l1l 												=												IIIlI1I1Il11 







                                                                                                                                                                                                                                                                                                                                  else 												:												









                                                                                                                                                                                                                                                                                                                                                         lI111l1l                              =                             lI1IlIll 






                                                                                                                                                                                                                                                                                                           if lI111l1l 												==												I1IlIlll11IIl1lII                        :                       





                                                                                                                                                                                                                                                                                                                                  lIllI1l11l 												=												IIlI1IlI 









                                                                                                                                                                                                                                                                                                           if lI111l1l 										==										lI1IlIll 																:																






                                                                                                                                                                                                                                                                                                                                  lIllI1l11l                            =                           I11I11l1 







                                                                                                                                                                                                                                                                                    if lIllI1l11l                          ==                         II11l1lI                            :                           




                                                                                                                                                                                                                                                                                                           Il1II1I1 										=										l111lIl1 




                                                                                                                                                                                                                                                                                                           lllIllI1                 =                IIIllIl1 

                                                                                                                                                                                                                                                                                                           llIlll11IlI1IlI1Il 								=								I1l1Il1l1lIl1IIl 








                                                                                                                                                                                                                                                                                                           if not lI1lI1Il11II1I 														(														lI1I1l11Ill                                 ,                                lllll1Il 															)																								:									


                                                                                                                                                                                                                                                                                                                                  llIlll11IlI1IlI1Il 														=														Il1l111lIl 

                                                                                                                                                                                                                                                                                                           else 										:										


                                                                                                                                                                                                                                                                                                                                  llIlll11IlI1IlI1Il                           =                          I11IIllI 




                                                                                                                                                                                                                                                                                                           if llIlll11IlI1IlI1Il 												==												Il1l111lIl 													:													









                                                                                                                                                                                                                                                                                                                                  if not I1lll1lI                        :                       





                                                                                                                                                                                                                                                                                                                                                         llIlll11IlI1IlI1Il                             =                            ll1l1lll 

                                                                                                                                                                                                                                                                                                                                  else 										:										


                                                                                                                                                                                                                                                                                                                                                         llIlll11IlI1IlI1Il                          =                         Il1lIl11 
                                                                                                                                                                                                                                                                                                           if llIlll11IlI1IlI1Il 									==									ll1I1IlI 														:														





                                                                                                                                                                                                                                                                                                                                  lllIllI1                       =                      II1IIl1l 




                                                                                                                                                                                                                                                                                                           if llIlll11IlI1IlI1Il                      ==                     I11IIllI 											:											
                                                                                                                                                                                                                                                                                                                                  lllIllI1 											=											Il1Il1IIlII11II1I 








                                                                                                                                                                                                                                                                                                           if lllIllI1 														==														llII111l                             :                            






                                                                                                                                                                                                                                                                                                                                  lll1l1II                     =                    Il111II1 





                                                                                                                                                                                                                                                                                                                                  if not IlllI11l 									(									l1lll1I1                               )                                                            :                              






                                                                                                                                                                                                                                                                                                                                                         lll1l1II                                =                               I1lll1lI 






                                                                                                                                                                                                                                                                                                                                  else 											:											


                                                                                                                                                                                                                                                                                                                                                         lll1l1II                            =                           lIIIIlll 







                                                                                                                                                                                                                                                                                                                                  if lll1l1II 										==										IllI1II1                         :                        

                                                                                                                                                                                                                                                                                                                                                         if not l11II1l1 												(												random                        .                       random 									(																						)																													,																IIll1llIlI111I11I1                                )                                                     :                      






                                                                                                                                                                                                                                                                                                                                                                                lll1l1II 														=														II1llIlI11ll1I 



                                                                                                                                                                                                                                                                                                                                                         else 															:															
                                                                                                                                                                                                                                                                                                                                                                                lll1l1II 													=													llll1111 



                                                                                                                                                                                                                                                                                                                                  if lll1l1II 									==									llll1111 												:												






                                                                                                                                                                                                                                                                                                                                                         lllIllI1                            =                           I1lllllI 





                                                                                                                                                                                                                                                                                                                                  if lll1l1II 										==										l1I1I1II                      :                     
                                                                                                                                                                                                                                                                                                                                                         lllIllI1 																=																I11I11II 




                                                                                                                                                                                                                                                                                                           if lllIllI1                        ==                       lI1Ill1l1Il1l1I 											:											



                                                                                                                                                                                                                                                                                                                                  pass 









                                                                                                                                                                                                                                                                                                           if lllIllI1 													==													I11I11II                                 :                                

                                                                                                                                                                                                                                                                                                                                  Il1II1I1 								=								random                          .                         choice                             (                                                    [                        l1IllI1I1l1lIlI1l                       ,                      l111IlIl                    ,                   Il1l1Illl11l1 											,											IlIlIIll                           ]                                                    )                          





                                                                                                                                                                                                                                                                                                           Ill1llII 																=																IIlI1IlI 





                                                                                                                                                                                                                                                                                                           III111                             =                            lIIlI1I1 






                                                                                                                                                                                                                                                                                                           if not IlllI11l                            (                           II1l1lIl11l1II                                 )                                                          :                          







                                                                                                                                                                                                                                                                                                                                  III111 									=									I1lI1l11 









                                                                                                                                                                                                                                                                                                           else 											:											
                                                                                                                                                                                                                                                                                                                                  III111                    =                   llll1II1 


                                                                                                                                                                                                                                                                                                           if III111 															==															l1IIll1I                              :                             








                                                                                                                                                                                                                                                                                                                                  if not l11II1l1                     (                    random                                .                               random 											(																											)																                ,                II1lll1l 																)																													:													



                                                                                                                                                                                                                                                                                                                                                         III111                                 =                                II1Il1Il 








                                                                                                                                                                                                                                                                                                                                  else                               :                              
                                                                                                                                                                                                                                                                                                                                                         III111 											=											IIIl1Il1 






                                                                                                                                                                                                                                                                                                           if III111                         ==                        I1lI1l11 									:									



                                                                                                                                                                                                                                                                                                                                  Ill1llII                         =                        Il1Il1IIlII11II1I 









                                                                                                                                                                                                                                                                                                           if III111 										==										IIIl1Il1 												:												
                                                                                                                                                                                                                                                                                                                                  Ill1llII 																=																I1lIlIIl 









                                                                                                                                                                                                                                                                                                           if Ill1llII 												==												Il1Il1IIlII11II1I 									:									







                                                                                                                                                                                                                                                                                                                                  I1l11Il1 									=									IIl1I1I1 






                                                                                                                                                                                                                                                                                                                                  if not I1I1I1lI                        (                       Il1Il1IIlII11II1I 									)																			:										





                                                                                                                                                                                                                                                                                                                                                         I1l11Il1 									=									IIIlI1IIII1 



                                                                                                                                                                                                                                                                                                                                  else                          :                         



                                                                                                                                                                                                                                                                                                                                                         I1l11Il1                  =                 Il11l1Il 





                                                                                                                                                                                                                                                                                                                                  if I1l11Il1                             ==                            IIIlI1IIII1                        :                       







                                                                                                                                                                                                                                                                                                                                                         if not l11II1l1 										(										I1IlI1l1                      ,                     IIIl11ll1l11lll11l                              )                                                        :                           








                                                                                                                                                                                                                                                                                                                                                                                I1l11Il1 															=															I111lII1 


                                                                                                                                                                                                                                                                                                                                                         else 													:													


                                                                                                                                                                                                                                                                                                                                                                                I1l11Il1                       =                      l1IIll1I 




                                                                                                                                                                                                                                                                                                                                  if I1l11Il1                           ==                          II1lll1I                             :                            




                                                                                                                                                                                                                                                                                                                                                         Ill1llII                       =                      II1lll1I 






                                                                                                                                                                                                                                                                                                                                  if I1l11Il1 									==									I1l1ll1Il111I1 														:														
                                                                                                                                                                                                                                                                                                                                                         Ill1llII 											=											ll11l11l 
                                                                                                                                                                                                                                                                                                           if Ill1llII 													==													l1Il1III 									:									



                                                                                                                                                                                                                                                                                                                                  pass 
                                                                                                                                                                                                                                                                                                           if Ill1llII                          ==                         I11I11l1l1l1 								:								



                                                                                                                                                                                                                                                                                                                                  Il1II1I1                                 =                                I1I1II11 



                                                                                                                                                                                                                                                                                                           lII11III 										=										IIlII1lII1IllI1I 







                                                                                                                                                                                                                                                                                                           IIl1llI 									=									II1Il1Il 




                                                                                                                                                                                                                                                                                                           if l11II1l1 											(											lIlI11lI                       ,                      IIIl11ll1l11lll11l                           )                          													:													
                                                                                                                                                                                                                                                                                                                                  IIl1llI                     =                    IlllI1I1 

                                                                                                                                                                                                                                                                                                           else                        :                       


                                                                                                                                                                                                                                                                                                                                  IIl1llI 								=								II11l1lI 








                                                                                                                                                                                                                                                                                                           if IIl1llI                  ==                 lllI1IlI                          :                         
                                                                                                                                                                                                                                                                                                                                  if l11II1l1                           (                          llIl1Ill                    ,                   I1l1I1II                  )                 															:															





                                                                                                                                                                                                                                                                                                                                                         IIl1llI                          =                         lI1III1l 







                                                                                                                                                                                                                                                                                                                                  else 														:														









                                                                                                                                                                                                                                                                                                                                                         IIl1llI                        =                       II1Il11l 








                                                                                                                                                                                                                                                                                                           if IIl1llI 												==												IIl11I1l 												:												




                                                                                                                                                                                                                                                                                                                                  lII11III 																=																I11I11l1l1l1 





                                                                                                                                                                                                                                                                                                           if IIl1llI 									==									l11lIIl1 															:															









                                                                                                                                                                                                                                                                                                                                  lII11III                        =                       I1lI11ll 
                                                                                                                                                                                                                                                                                                           if lII11III 													==													I1lI11ll 															:															

                                                                                                                                                                                                                                                                                                                                  I1111I1l 															=															Il1III1I 


                                                                                                                                                                                                                                                                                                                                  if l1111ll1                                 (                                lIlIII11                            ,                           l11lll1I                             -                            ll1l111l                        )                                              :                       




                                                                                                                                                                                                                                                                                                                                                         I1111I1l 											=											lllll1Il 



                                                                                                                                                                                                                                                                                                                                  else                          :                         




                                                                                                                                                                                                                                                                                                                                                         I1111I1l 										=										l11lII1I 
                                                                                                                                                                                                                                                                                                                                  if I1111I1l                        ==                       I1lll1lI                         :                        






                                                                                                                                                                                                                                                                                                                                                         if not I1I1I1lI 								(								Ill1I1I1 															)															                             :                             





                                                                                                                                                                                                                                                                                                                                                                                I1111I1l 										=										I111IIIlI111I11ll 






                                                                                                                                                                                                                                                                                                                                                         else                         :                        







                                                                                                                                                                                                                                                                                                                                                                                I1111I1l                           =                          Il1l1ll1 




                                                                                                                                                                                                                                                                                                                                  if I1111I1l                                ==                               lI1Ill1l                           :                          



                                                                                                                                                                                                                                                                                                                                                         lII11III 													=													I11I11l1l1l1 








                                                                                                                                                                                                                                                                                                                                  if I1111I1l 																==																IlI1IIIlIlI1I11l1llI 																:																







                                                                                                                                                                                                                                                                                                                                                         lII11III                             =                            IllIIl1I 







                                                                                                                                                                                                                                                                                                           if lII11III                              ==                             IllIIl1I 									:									








                                                                                                                                                                                                                                                                                                                                  l11lll11 								.								append                 (                f'Vec3({Il11IIIl},{lIlIII11},{llI1IllI}):GrassBlock'                            )                            



                                                                                                                                                                                                                                                                                                                                  break 









                                                                                                                                                                                                                                                                                                           if lII11III                       ==                      lI1lII1l                          :                         





                                                                                                                                                                                                                                                                                                                                  ll111I11 													=													IllI1II1 





                                                                                                                                                                                                                                                                                                                                  I111llI1                  =                 II1I1IlI 
                                                                                                                                                                                                                                                                                                                                  if lIlllIIl 										(										lIlIII11 										,										l11lll1I 												-												llIIl1l1                            )                           											:											

                                                                                                                                                                                                                                                                                                                                                         I111llI1 															=															II1Il1Il 





                                                                                                                                                                                                                                                                                                                                  else                            :                           




                                                                                                                                                                                                                                                                                                                                                         I111llI1 															=															Il1lI11I 





                                                                                                                                                                                                                                                                                                                                  if I111llI1                    ==                   I1lI1l11                                :                               




                                                                                                                                                                                                                                                                                                                                                         if not IIl11I1l 												:												
                                                                                                                                                                                                                                                                                                                                                                                I111llI1 													=													llllIIll 
                                                                                                                                                                                                                                                                                                                                                         else 										:										


                                                                                                                                                                                                                                                                                                                                                                                I111llI1                   =                  ll1II1I1 


                                                                                                                                                                                                                                                                                                                                  if I111llI1 											==											l1I1I1II 								:								




                                                                                                                                                                                                                                                                                                                                                         ll111I11 													=													lllII1Il 









                                                                                                                                                                                                                                                                                                                                  if I111llI1 														==														lll1II1I 													:													







                                                                                                                                                                                                                                                                                                                                                         ll111I11                         =                        lII1lI1l 








                                                                                                                                                                                                                                                                                                                                  if ll111I11                       ==                      lII1lI1l 										:										






                                                                                                                                                                                                                                                                                                                                                         I1l1ll1l 										=										Il1lIl11 




                                                                                                                                                                                                                                                                                                                                                         if not ll1III 															:															









                                                                                                                                                                                                                                                                                                                                                                                I1l1ll1l 													=													l11lII1I 


                                                                                                                                                                                                                                                                                                                                                         else 										:										







                                                                                                                                                                                                                                                                                                                                                                                I1l1ll1l 											=											IlIl1III 

                                                                                                                                                                                                                                                                                                                                                         if I1l1ll1l 																==																l11lII1I                         :                        








                                                                                                                                                                                                                                                                                                                                                                                if not IlllI11l 														(														IlI1II1I                         )                                        :                





                                                                                                                                                                                                                                                                                                                                                                                                       I1l1ll1l 									=									llIIl11I 









                                                                                                                                                                                                                                                                                                                                                                                else                     :                    





                                                                                                                                                                                                                                                                                                                                                                                                       I1l1ll1l                         =                        lI1Ill1l1Il1l1I 




                                                                                                                                                                                                                                                                                                                                                         if I1l1ll1l 														==														IIlll1II                           :                          









                                                                                                                                                                                                                                                                                                                                                                                ll111I11                           =                          l1lII1l1 







                                                                                                                                                                                                                                                                                                                                                         if I1l1ll1l 															==															lIl1llII                             :                            





                                                                                                                                                                                                                                                                                                                                                                                ll111I11 								=								ll1III 









                                                                                                                                                                                                                                                                                                                                  if ll111I11                              ==                             ll1III 															:															



                                                                                                                                                                                                                                                                                                                                                         pass 


                                                                                                                                                                                                                                                                                                                                  if ll111I11 									==									II11I11I 											:											



                                                                                                                                                                                                                                                                                                                                                         l11lll11 											.											append                       (                      f'Vec3({Il11IIIl},{lIlIII11},{llI1IllI}):DirtBlock'                            )                            




                                                                                                                                                                                                                                                                                                                                                         continue 








                                                                                                                                                                                                                                                                                                           l11lll11 								.								append 														(														f'Vec3({Il11IIIl},{lIlIII11},{llI1IllI}):{Il1II1I1}'                    )                    

                                                                                                                                                                                                                                                                                    if lIllI1l11l                     ==                    II1Il1Il                          :                         







                                                                                                                                                                                                                                                                                                           pass 
                                                                                                                                                                                                                                      l11lll11                   .                  append 												(												f'Vec3({Il11IIIl},-5,{llI1IllI}):BedrockBlock'											)											




                                                                                                                                                                                                                                      while                 (                															(															not I1I1I1lI                          (                         ll11l11l                           )                          or not Illll1Il                  )                 or 									(									lI11IlII or not IlllI11l                              (                             IlI1lll1 									)																	)								                              )                              and 																(																I1lI1I1l1Ill1 													>=													lI111lII and I1ll11lI 									>=									l1llIIlI or 															(															IlllI11l                                 (                                lllll1Il 															)															and l1I1l1l1                       )                                          )                                                 :                             



                                                                                                                                                                                                                                                             for II1lIl1l in Il1llllI 																(																lIIIlllI                           ,                          IIlIIIIl 													)													                  :                  








                                                                                                                                                                                                                                                                                    for lIlIII11 in Il1llllI                                 (                                													-													I1IlIlll11IIl1lII                    ,                   l1lIlII1 																)																															:															




                                                                                                                                                                                                                                                                                                           II1ll1ll                   =                  lllI1IlI 









                                                                                                                                                                                                                                                                                                           I1llI1Il 													=													IIlI1Ill 





                                                                                                                                                                                                                                                                                                           if not lI1lI1l1lI1l1lll1II 													.													lIIlIl11                          (                         I1lIII11                        )                       								:								

                                                                                                                                                                                                                                                                                                                                  I1llI1Il                              =                             Il11l1Il 









                                                                                                                                                                                                                                                                                                           else 											:											
                                                                                                                                                                                                                                                                                                                                  I1llI1Il 															=															IIlIIIIl 







                                                                                                                                                                                                                                                                                                           if I1llI1Il 								==								IIlIIIIl                        :                       




                                                                                                                                                                                                                                                                                                                                  II1ll1lI 												=												lI111Il1l1 
                                                                                                                                                                                                                                                                                                                                  lIlIlIIl 									=									Il1ll11I 


                                                                                                                                                                                                                                                                                                                                  lI11Il1I                            =                           IllI1lIl 


                                                                                                                                                                                                                                                                                                                                  if not I1I1I1lI                             (                            I1I111IlI111I1lll 								)								                    :                    







                                                                                                                                                                                                                                                                                                                                                         lI11Il1I 															=															IIlIll1l 








                                                                                                                                                                                                                                                                                                                                  else 													:													



                                                                                                                                                                                                                                                                                                                                                         lI11Il1I 										=										ll1l1I 






                                                                                                                                                                                                                                                                                                                                  if lI11Il1I 										==										I1l111I1 																:																




                                                                                                                                                                                                                                                                                                                                                         if lI1Il11I 											(											I1l1I1II                  ,                 Il1III1I                           )                          										:										







                                                                                                                                                                                                                                                                                                                                                                                lI11Il1I                                 =                                Il1l111lIl 


                                                                                                                                                                                                                                                                                                                                                         else                    :                   





                                                                                                                                                                                                                                                                                                                                                                                lI11Il1I                   =                  I111l1ll 

                                                                                                                                                                                                                                                                                                                                  if lI11Il1I                    ==                   Il1l111lIl                 :                






                                                                                                                                                                                                                                                                                                                                                         lIlIlIIl                 =                Il1I1ll1 

                                                                                                                                                                                                                                                                                                                                  if lI11Il1I 														==														IIlIll1l                       :                      

                                                                                                                                                                                                                                                                                                                                                         lIlIlIIl                         =                        I1llllIlIIl1II 






                                                                                                                                                                                                                                                                                                                                  if lIlIlIIl 										==										I1llllIlIIl1II 									:									


                                                                                                                                                                                                                                                                                                                                                         IIII1l11 									=									lIl11111 




                                                                                                                                                                                                                                                                                                                                                         if not I1I1I1lI                           (                          Illll1lI 											)											                :                



                                                                                                                                                                                                                                                                                                                                                                                IIII1l11 										=										llIIl11IIlllIl1 



                                                                                                                                                                                                                                                                                                                                                         else                           :                          






                                                                                                                                                                                                                                                                                                                                                                                IIII1l11 											=											Ill1111I 








                                                                                                                                                                                                                                                                                                                                                         if IIII1l11                   ==                  IIlIll1l 														:														

                                                                                                                                                                                                                                                                                                                                                                                if not II1I1lll 															:															




                                                                                                                                                                                                                                                                                                                                                                                                       IIII1l11                                =                               IlI1Il11 



                                                                                                                                                                                                                                                                                                                                                                                else 														:														







                                                                                                                                                                                                                                                                                                                                                                                                       IIII1l11                             =                            lIlI111lII1II1ll 


                                                                                                                                                                                                                                                                                                                                                         if IIII1l11                              ==                             lllI1lll                      :                     

                                                                                                                                                                                                                                                                                                                                                                                lIlIlIIl                      =                     IIIlI1I1Il11 







                                                                                                                                                                                                                                                                                                                                                         if IIII1l11                          ==                         IlI1Il11                    :                   




                                                                                                                                                                                                                                                                                                                                                                                lIlIlIIl 											=											l11I1llI 
                                                                                                                                                                                                                                                                                                                                  if lIlIlIIl                             ==                            l11I1llI 										:										
                                                                                                                                                                                                                                                                                                                                                         II1ll1lI                         =                        ll1l1111 





                                                                                                                                                                                                                                                                                                                                  if lIlIlIIl 														==														I1IlIlll11IIl1lII 															:															









                                                                                                                                                                                                                                                                                                                                                         II1ll1lI                               =                              lll111II 
                                                                                                                                                                                                                                                                                                                                  if II1ll1lI 								==								lll111II 																:																




                                                                                                                                                                                                                                                                                                                                                         IIl11IlI 														=														lI1l1Ill 







                                                                                                                                                                                                                                                                                                                                                         I1IlII1l                       =                      IlI1Il11 


                                                                                                                                                                                                                                                                                                                                                         if not I1I1I1lI                          (                         I1lI1I1l1Ill1 																)																														:														






                                                                                                                                                                                                                                                                                                                                                                                I1IlII1l                              =                             IIllIIl1 

                                                                                                                                                                                                                                                                                                                                                         else 												:												



                                                                                                                                                                                                                                                                                                                                                                                I1IlII1l 									=									ll1lI1 


                                                                                                                                                                                                                                                                                                                                                         if I1IlII1l                              ==                             ll1II1I1 																:																
                                                                                                                                                                                                                                                                                                                                                                                if not IlllI11l                       (                      llII1lI1                  )                                      :                     







                                                                                                                                                                                                                                                                                                                                                                                                       I1IlII1l                     =                    lI111Il1l1 





                                                                                                                                                                                                                                                                                                                                                                                else 									:									






                                                                                                                                                                                                                                                                                                                                                                                                       I1IlII1l 											=											l1lI1ll1 



                                                                                                                                                                                                                                                                                                                                                         if I1IlII1l 															==															l1lI1ll1 										:										



                                                                                                                                                                                                                                                                                                                                                                                IIl11IlI 									=									ll1I1IlI 








                                                                                                                                                                                                                                                                                                                                                         if I1IlII1l 											==											I1l1l11I 										:										
                                                                                                                                                                                                                                                                                                                                                                                IIl11IlI 														=														lI1II1l1 




                                                                                                                                                                                                                                                                                                                                                         if IIl11IlI 														==														IlI1Il11                             :                            


                                                                                                                                                                                                                                                                                                                                                                                II1I1l111l11111                  =                 l1ll11Il 






                                                                                                                                                                                                                                                                                                                                                                                if not l1Il1III 												:												

                                                                                                                                                                                                                                                                                                                                                                                                       II1I1l111l11111 									=									llIl1Ill 








                                                                                                                                                                                                                                                                                                                                                                                else                 :                









                                                                                                                                                                                                                                                                                                                                                                                                       II1I1l111l11111                        =                       IIIllIl1 
                                                                                                                                                                                                                                                                                                                                                                                if II1I1l111l11111                    ==                   lIlI111lII1II1ll 												:												








                                                                                                                                                                                                                                                                                                                                                                                                       if not Il1IlI1ll 											:											







                                                                                                                                                                                                                                                                                                                                                                                                                              II1I1l111l11111 									=									IIIIIIl1 






                                                                                                                                                                                                                                                                                                                                                                                                       else 								:								

                                                                                                                                                                                                                                                                                                                                                                                                                              II1I1l111l11111 												=												I11IlllI 





                                                                                                                                                                                                                                                                                                                                                                                if II1I1l111l11111 										==										I11IlllI 															:															

                                                                                                                                                                                                                                                                                                                                                                                                       IIl11IlI                                 =                                ll1I1IlI 




                                                                                                                                                                                                                                                                                                                                                                                if II1I1l111l11111                 ==                l1I1l1l1 												:												








                                                                                                                                                                                                                                                                                                                                                                                                       IIl11IlI 																=																ll11lIII 







                                                                                                                                                                                                                                                                                                                                                         if IIl11IlI 											==											III1lIlI1llI1l 								:								









                                                                                                                                                                                                                                                                                                                                                                                II1ll1lI                          =                         I1lI11ll 









                                                                                                                                                                                                                                                                                                                                                         if IIl11IlI 										==										I1111lI1111Il1lI11                  :                 


                                                                                                                                                                                                                                                                                                                                                                                II1ll1lI 												=												IlllI1Il 

                                                                                                                                                                                                                                                                                                                                  if II1ll1lI 										==										ll1IIIl1Il 													:													




                                                                                                                                                                                                                                                                                                                                                         I1llI1Il                                =                               lI1lII1l 





                                                                                                                                                                                                                                                                                                                                  if II1ll1lI 								==								I1I11111                   :                  


                                                                                                                                                                                                                                                                                                                                                         I1llI1Il 																=																I11IlllI 




                                                                                                                                                                                                                                                                                                           if I1llI1Il 																==																I11IlllI 												:												

                                                                                                                                                                                                                                                                                                                                  II1ll1ll 									=									lIIlIlIIlIlllIIl1 








                                                                                                                                                                                                                                                                                                           if I1llI1Il                              ==                             lIIII1III111 														:														








                                                                                                                                                                                                                                                                                                                                  II1ll1ll 											=											Il111II1 







                                                                                                                                                                                                                                                                                                           if II1ll1ll 								==								Il1III1I 																:																



                                                                                                                                                                                                                                                                                                                                  l111II1Il1I                  =                 Il1I11l1 






                                                                                                                                                                                                                                                                                                                                  if not lI1lI1l1lI1l1lll1II 															.															lIIlIl11                                 (                                I1ll11lI 													)																										:													





                                                                                                                                                                                                                                                                                                                                                         l111II1Il1I                       =                      llII1Ill 


                                                                                                                                                                                                                                                                                                                                  else                        :                       




                                                                                                                                                                                                                                                                                                                                                         l111II1Il1I                    =                   Il1ll1l1 







                                                                                                                                                                                                                                                                                                                                  if l111II1Il1I 												==												IIIlI1IIII1 														:														









                                                                                                                                                                                                                                                                                                                                                         if lI1lI1Il11II1I                         (                        Il11l1ll 								,								Il1IlI11 															)																														:															
                                                                                                                                                                                                                                                                                                                                                                                l111II1Il1I                          =                         IIIl1Il1 






                                                                                                                                                                                                                                                                                                                                                         else 											:											


                                                                                                                                                                                                                                                                                                                                                                                l111II1Il1I 														=														lIIlllI1 

                                                                                                                                                                                                                                                                                                                                  if l111II1Il1I 																==																lI11IlII                        :                       






                                                                                                                                                                                                                                                                                                                                                         II1ll1ll 														=														llll1111 


                                                                                                                                                                                                                                                                                                                                  if l111II1Il1I                                ==                               ll11lIll 														:														


                                                                                                                                                                                                                                                                                                                                                         II1ll1ll 									=									III1lIlI1llI1l 






                                                                                                                                                                                                                                                                                                           if II1ll1ll 															==															I1lIl1lI                    :                   







                                                                                                                                                                                                                                                                                                                                  l11lll11                         .                        append                           (                          f'Vec3({Il11IIIl},{lIlIII11},{llI1IllI}):StoneBlock'											)											






                                                                                                                                                                                                                                                                                                           if II1ll1ll 											==											l11lII1I 																:																





                                                                                                                                                                                                                                                                                                                                  pass 



                                                                                                                                                                                                                                                             break 








                                                                     with lIl11lllIlll111Il                  (                 conf_path                     (                    											)											                              +                              lI1II1I1                              .                             format                     (                    lll11I1I                              )                             									,									II11ll11Ill                            )                           as I1l1Il1l                 :                









                                                                                            for lIlllIll in lIIlI1IIIIIII1                 (                lI1l11I1                  ,                 IlIl1III 																)																                      :                      






                                                                                                                   for llIIlIl1lIIllll in l11lll11                             :                            
                                                                                                                                          II1II1lI 										=										l11lI1II 
                                                                                                                                          llIlI1l1                         =                        I1lI1l11 








                                                                                                                                          if l1111ll1 													(													III1Il1I 													,													II11l1I1 										)																									:															





                                                                                                                                                                 llIlI1l1                   =                  l1I1I1II 








                                                                                                                                          else                     :                    
                                                                                                                                                                 llIlI1l1 													=													llIl1Ill 








                                                                                                                                          if llIlI1l1 														==														lllI1lll 										:										



                                                                                                                                                                 if not llI1Il1ll1I1l1I1IIll 											:											



                                                                                                                                                                                        llIlI1l1                               =                              l11lIIl1 
                                                                                                                                                                 else                           :                          








                                                                                                                                                                                        llIlI1l1                      =                     IllIIl1I 








                                                                                                                                          if llIlI1l1                  ==                 ll1II1I1 										:										




                                                                                                                                                                 II1II1lI 											=											IIl1I1I1 

                                                                                                                                          if llIlI1l1 									==									lI1IlIll 												:												






                                                                                                                                                                 II1II1lI 											=											l11lI1Il 






                                                                                                                                          if II1II1lI 															==															l11lI1Il                        :                       



                                                                                                                                                                 lIlIl1                                =                               I1lllllI 









                                                                                                                                                                 if not I1I1I1lI 												(												l1III1l1                             )                            													:													





                                                                                                                                                                                        lIlIl1 									=									lII1ll1l 








                                                                                                                                                                 else 											:											


                                                                                                                                                                                        lIlIl1 														=														Illll1Il 






                                                                                                                                                                 if lIlIl1                              ==                             I1ll1ll1                           :                          




                                                                                                                                                                                        Ill1II1I 													=													llII1lll 






                                                                                                                                                                                        lIIl111l                             =                            IIIIl1lI 





                                                                                                                                                                                        ll11IIl1 										=										l1IlIl1I 







                                                                                                                                                                                        if not I1I1I1lI 																(																l1I1I11l                        )                       														:														



                                                                                                                                                                                                               ll11IIl1 								=								I1IIl1Il 





                                                                                                                                                                                        else                      :                     
                                                                                                                                                                                                               ll11IIl1 														=														I11l1I1l 









                                                                                                                                                                                        if ll11IIl1                              ==                             IllI11llII1 													:													


                                                                                                                                                                                                               if not ll1l1lll 									:									

                                                                                                                                                                                                                                      ll11IIl1 												=												I11l1I1l 




                                                                                                                                                                                                               else 													:													




                                                                                                                                                                                                                                      ll11IIl1 								=								I1IIl11l 







                                                                                                                                                                                        if ll11IIl1                    ==                   IlIIllIl                 :                








                                                                                                                                                                                                               lIIl111l                         =                        lI111Il1l1 


                                                                                                                                                                                        if ll11IIl1 									==									I1ll1ll1 													:													
                                                                                                                                                                                                               lIIl111l                    =                   II1I1IlI 
                                                                                                                                                                                        if lIIl111l 													==													lI111Il1l1                     :                    








                                                                                                                                                                                                               Il1I1llI                          =                         l1lII1l1 



                                                                                                                                                                                                               if not I1I1I1lI                    (                   I1lll1lI                       )                                           :                     






                                                                                                                                                                                                                                      Il1I1llI                          =                         ll1I1IlI 




                                                                                                                                                                                                               else                     :                    






                                                                                                                                                                                                                                      Il1I1llI 								=								Il11l1ll 




                                                                                                                                                                                                               if Il1I1llI 														==														ll1I1IlI 																:																





                                                                                                                                                                                                                                      if not I11IIlI1                          :                         





                                                                                                                                                                                                                                                             Il1I1llI                            =                           Il11l1ll 


                                                                                                                                                                                                                                      else                 :                









                                                                                                                                                                                                                                                             Il1I1llI                    =                   II1Illl1 









                                                                                                                                                                                                               if Il1I1llI                            ==                           llI1I111 								:								
                                                                                                                                                                                                                                      lIIl111l                    =                   l1lIIl11 




                                                                                                                                                                                                               if Il1I1llI 								==								l1lIIlll 								:								



                                                                                                                                                                                                                                      lIIl111l                            =                           IIIlI1IIII1 



                                                                                                                                                                                        if lIIl111l 										==										IIIlI1IIII1 																:																

                                                                                                                                                                                                               Ill1II1I 															=															IIlI1lI1 

                                                                                                                                                                                        if lIIl111l                               ==                              l1lIIl11                              :                             






                                                                                                                                                                                                               Ill1II1I                         =                        IlIllIIlI1 
                                                                                                                                                                                        if Ill1II1I                  ==                 I1l1llIl 								:								

                                                                                                                                                                                                               III1II11                    =                   IIlI11II 






                                                                                                                                                                                                               l1IlIlII                       =                      lI111l11 




                                                                                                                                                                                                               if not I1I1I1lI 													(													I111ll1l 													)																								:											





                                                                                                                                                                                                                                      l1IlIlII 										=										IIllIll1 

                                                                                                                                                                                                               else                       :                      






                                                                                                                                                                                                                                      l1IlIlII 																=																Ill1111I 



                                                                                                                                                                                                               if l1IlIlII 														==														Ill1111I 									:									

                                                                                                                                                                                                                                      if lI1Il11I                      (                     lI11IlII 																,																II1I11Il 															)															                 :                 

                                                                                                                                                                                                                                                             l1IlIlII                  =                 llI1l1ll 




                                                                                                                                                                                                                                      else 										:										



                                                                                                                                                                                                                                                             l1IlIlII                                =                               Ill1II1I1l1II1 


                                                                                                                                                                                                               if l1IlIlII                      ==                     ll1IIIl1Il                  :                 
                                                                                                                                                                                                                                      III1II11                              =                             llIllI111111111 






                                                                                                                                                                                                               if l1IlIlII 																==																IIllIll1 										:										



                                                                                                                                                                                                                                      III1II11                     =                    lIll11l1 



                                                                                                                                                                                                               if III1II11 															==															IlI1IIIlIlI1I11l1llI                          :                         









                                                                                                                                                                                                                                      I1l1l1IIlIlIIII1Ill 																=																Il11l1ll 
                                                                                                                                                                                                                                      if not IIlIIIIl                   :                  







                                                                                                                                                                                                                                                             I1l1l1IIlIlIIII1Ill                               =                              I1ll1ll1 



                                                                                                                                                                                                                                      else 											:											





                                                                                                                                                                                                                                                             I1l1l1IIlIlIIII1Ill                              =                             lll1Il11 



                                                                                                                                                                                                                                      if I1l1l1IIlIlIIII1Ill                   ==                  lll1Il11                               :                              







                                                                                                                                                                                                                                                             if l11II1l1                    (                   lIllI1l1                   ,                  l1l1111lI1IIl1ll11 															)															                           :                           

                                                                                                                                                                                                                                                                                    I1l1l1IIlIlIIII1Ill                       =                      lI11lIll 








                                                                                                                                                                                                                                                             else 												:												





                                                                                                                                                                                                                                                                                    I1l1l1IIlIlIIII1Ill 												=												l1lIIl11 







                                                                                                                                                                                                                                      if I1l1l1IIlIlIIII1Ill                           ==                          IlI1lll1 									:									



                                                                                                                                                                                                                                                             III1II11                   =                  lIll11l1 


                                                                                                                                                                                                                                      if I1l1l1IIlIlIIII1Ill                                 ==                                Illll1Il 									:									







                                                                                                                                                                                                                                                             III1II11 												=												II11ll1IlI 






                                                                                                                                                                                                               if III1II11 																==																IIl11I1l                              :                             

                                                                                                                                                                                                                                      Ill1II1I 														=														IIlIlIl1 
                                                                                                                                                                                                               if III1II11 																==																lIll11l1                                 :                                
                                                                                                                                                                                                                                      Ill1II1I                         =                        IIIIIIl1 
                                                                                                                                                                                        if Ill1II1I                   ==                  lI1l11lIII1ll                              :                             



                                                                                                                                                                                                               lIlIl1 																=																I1ll1I1l 
                                                                                                                                                                                        if Ill1II1I 										==										I11Il1                              :                             






                                                                                                                                                                                                               lIlIl1                              =                             IlI1II1I 


                                                                                                                                                                 if lIlIl1                     ==                    ll1lIlI1 													:													






                                                                                                                                                                                        II1II1lI 										=										IlIIIlI1 









                                                                                                                                                                 if lIlIl1                                 ==                                IIIlI11lllIl                     :                    






                                                                                                                                                                                        II1II1lI 										=										lI1I1l11Ill 

                                                                                                                                          if II1II1lI 											==											IIIl1ll1 								:								







                                                                                                                                                                 pass 

                                                                                                                                          if II1II1lI                               ==                              lI1I1l11Ill 								:								






                                                                                                                                                                 I1l1Il1l 															.															write                     (                    llIIlIl1lIIllll                             +                            Il1lIl1I                  )                 



                                                                     Il11l1111IIllI1llll 								.								__finish_generation                            (                           world_name                   =                  lll11I1I                      ,                     seed 									=									l1ll1IlI 										,										world_size                             =                            I1II1l11 											)											





                                              except WORLD_GENERATOR_STATUS                    .                   INVALID_WORLD_NAME 								:								
                                                                     Il11l1111IIllI1llll 														.														progression                           =                          													-													IIl1l1Il 





                                              except WORLD_GENERATOR_STATUS 								.								EMPTY_WORLD_NAME                     :                    


                                                                     Il11l1111IIllI1llll 								.								progression                            =                           											-											Illll1lI 






                                              except WORLD_GENERATOR_STATUS 															.															OS_ERROR 									:									


                                                                     Il11l1111IIllI1llll                   .                  progression                   =                  															-															l1III1Il 




                                              except WORLD_GENERATOR_STATUS 													.													WORLD_SIZE_0 													:													


                                                                     Il11l1111IIllI1llll 								.								progression 																=																													-													II11IIll 
                                              except Exception as e                  :                 

                                                                     Il11l1111IIllI1llll                       .                      progression                               =                              													-													I1IIl1I1 









                       def get_progression 																(																self 											)											                     ->                     int 																:																









                                              return l1IIlI                                 (                                self 											)											








                       def __finish_generation                  (                 self                         ,                        world_name                                :                               str                         ,                        seed                       :                      str                         ,                        world_size                         :                        str 											)																							->												None 													:													




                                              (															IIlI1l1I 														,														ll1lII11                             ,                            lI1llIlI 												,												lIIIIII1 											)																											=																                               (                               seed                 ,                world_name 								,								self 															,															world_size                      )                     









                                              with l1lI1l11                     (                    conf_path 													(													                   )                   															+															l1Ill1I1 								.								format 										(										ll1lII11                         )                                                    ,                            II11ll11Ill                    )                   as l1Il11                       :                      

                                                                     l1Il11                          .                         write                   (                  f"Wait... You really thought you could get your worlds infos...\nYou don't know who am I :,)"											)											


                                              lI1llIlI                  .                 progression                          =                         I1IIl1I1 


class WorldSize0                  (                 Exception                           )                          											:											







                       pass 