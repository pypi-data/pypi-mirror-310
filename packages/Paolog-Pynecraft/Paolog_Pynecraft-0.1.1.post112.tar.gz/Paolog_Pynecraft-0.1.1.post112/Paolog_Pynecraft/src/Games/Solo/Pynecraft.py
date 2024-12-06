from ursina import 														*														






from 								.								Entities 															.															Player                         .                        Player import Player 




from math import atan2 








import time 

from ursina import random                 ,                pi 









from                        ...                       UI                         .                        button import PyneButton 




from 								...								UI                  .                 bar import PyneBar 
from                  ...                 other 																.																quit import PyneQuit 








from threading import Thread 



import random 







import os 







import codecs 
(                               lIll1II1                            ,                           Il11111l 													,													I11I1IlI                 ,                IllIIII1                       ,                      IIll1I1I                           ,                          II11111I                           ,                          IlIIl1I1 								,								ll1111lI                         ,                        I1l1I11I 																,																Ill11I11 									,									ll1ll1Il 															,															Ill111l1                               ,                              l1I1lII1                     ,                    l1I11l1l                       ,                      II1I111I                  ,                 I1l11Ill                                ,                               l11ll1I1                 ,                IlIlI1II 									,									Il1lIlI1 												,												IIIIllll                                ,                               l1l1Illl 																,																lIIl1Ill 										,										I1IlIIII                          ,                         IIIIIlI1 												,												III1lllI                    ,                   IIII11II                             ,                            I1IllIII                 ,                l111I11I 											,											I1lllIIl 										,										l11I1I1I 																,																lI11llll 										,										IIII1IlI 																,																I1lll11I 																,																IlIlIl11 															,															ll11IlI1 																,																l1llIl1l                                ,                               I111l1Il                            ,                           lIIlllIl 										,										IllIl111 												,												IIlIl1I1                    ,                   ll11IlII                                 ,                                l111lII1 												,												IlIIIlIl 								,								Ill1lI1l                               ,                              I1l1llII 														,														I1I11Il1 									,									l1I1llII 									,									lIl1II11 													,													lIlIl1ll                 ,                I1I1ll11 														,														Il11IlIl                                ,                               ll1l11II 															,															IIIlI1                 ,                lllIIIll                     ,                    lIllIIlI 											,											II1l1lII                    ,                   IIl1lllI                          ,                         IIlIIll1                     ,                    Il11l1II 														,														l11111Il 									,									l11l11l1 									,									I1l1ll11 													,													l1Il1I1I 											,											II111lIl                   ,                  lllI1ll1 																,																l1lIIllI 								,								lI1l111I 															,															II1I11ll 												,												I1lIl1ll                            ,                           IIlIlIlI                                ,                               l1lI1lI1                        ,                       III1111l                  ,                 II11Il1I 																,																l1111llI 									,									l1ll1Il1 								,								Il1l1IIl 															,															llIl1I11 																,																Il11lI1l                              ,                             lIIlll1l                          ,                         lIl1l1lI                            ,                           I11l1II1 												,												lIlll1I1                       ,                      l1I1lI1I 									,									l1I1lIlI                           ,                          l1IlIlI1                                 ,                                IllIlIll                              ,                             II1lI1l1 													,													l1I11ll1                                 ,                                I111l111                 ,                lIl1I1l1                 ,                ll11Ill1 												,												l1ll1llI                        ,                       l1llIll1                       ,                      lIlIlIll 																,																l1l1ll1I                                ,                               lIIll1II                        ,                       lIIIIlII                                ,                               ll1III1I 														,														I11IIIll 								,								IIl11II1 														,														l11111II                   ,                  l1l1IIIl                                 ,                                IllIll1l 															,															Il111l1I 																,																IIll1IlI                    ,                   l1l1lllI                      ,                     ll11IlIl 																,																III11Il1 									,									l11l1lII 										,										lIlI1II1 													,													Il11I111 									,									lIlIl111                   ,                  IIllIlIl                            ,                           I1lI1lIl                     ,                    l111I11l                       ,                      I1l1Il11                     ,                    II11IlIl                             ,                            l1l1IlIl 											,											ll1111l1                      ,                     ll111I1l 											,											ll1lll1l                           ,                          IlIlIll1 															,															llII1llI                              ,                             l1lIl1ll 																,																IlI1IIII                    ,                   IlII111l 														,														lI1lI1I1                                 ,                                llIlIIIl 									,									Il11Ill1 											,											l1l1Ill1 									,									IIII11ll 													,													l1Il1111 														,														lIl1I11l                 ,                l11111ll                      ,                     IIl1I1ll 								,								IIIll1Il                         ,                        llllI1lI                         ,                        II1Il1ll                  ,                 lII1lIlI                       ,                      llI11llI                           ,                          lI1II1Il                        ,                       lI1lIlIl                            ,                           llllIlIl                     ,                    l1IIllI1                      ,                     lll11IIl 													,													IIIllI1I                        ,                       lIl111II                         ,                        lIl1lII1 													,													Il11l111                           ,                          l111111I                     ,                    IlI1lIIl                             ,                            III1IlII 								,								IlI1ll1l                           ,                          lllllIll 										,										ll1llIl1 											,											lIl1IIIl 										,										I1II11l1                               ,                              II111I1I                            ,                           I1llll1l 														,														Ill1l1I1 											,											IIlI111I                                ,                               IIII1IIl 									,									I1l1III1 									,									llIII1lI                   ,                  IIllIlI1 											,											IIlIl11l                    ,                   l1llIIIl                                ,                               IIl1llI1 													,													ll11lI11                   ,                  II11IIlI 									,									IIIl1111 													,													llll1I11 										,										Il1llIIl 												,												I1IllllI 									,									lllIII1l                              ,                             lIl1lIll 									,									IllI11II 															,															II1Ill1I 									,									l11Il1II 															,															l11lIlII                          ,                         Ill1l1l1                                 ,                                IllI1ll1                        ,                       I11l111l                               ,                              lI1llI11 												,												l1l111l1 															,															lIl1IlIl 												,												IIIlI1lI                 ,                II111Il1                            ,                           l1I1Il11                     ,                    II1l1Il1 									,									I111II1I                 ,                lIlIlll1 								,								II1Il1lI                             ,                            I1lIlI1I 										,										I11III1l 											,											lI11lIIl                               ,                              lIlI11I1 											,											l1III11I                    ,                   IIl1l111                 ,                I1IIII11                               ,                              l1l11Il1 										,										I1I1IlII                    ,                   I11IlI1l 										,										III1llI1 															,															l1llllI1 														,														I1l1II1l                      ,                     I11IIll1 																,																I1I11IIl 										,										II11Illl                      ,                     l1llIIl1                              ,                             l1llIl1I                          ,                         ll1II1ll                        ,                       l111l1lI                     ,                    Il111IlI 										,										lIlll1lI 										,										Ill1II1l 												,												II1IlI1l                          ,                         IlI1lllI 											,											I1l1I1I1 																,																Il11llll 														,														lI1IlI11 												,												IllIlI1l 										,										l1I11II1 															,															IlIIl1ll                              ,                             lIII1II1 								,								II1lllII 								,								Il1Il1I1 														,														I111l1lI 												,												lIIl1lI1                              ,                             I1I1lII1 												,												II1III1I                            ,                           l1llIIll                                ,                               lI1Ill11                  ,                 lI1Il1ll 												,												Ill11llI 											,											lI1ll111                   ,                  IlIllll1 															,															IIll11I1 										,										Il1IllIl 													,													lI11ll1I                                ,                               lIll1Ill                           ,                          lIIl11II                            ,                           I1IlII11                                 ,                                IllI1l1I 									,									l1l1lIl1 													,													IIlIIlll                               ,                              lllI1l1l 																,																llII1l1l 														,														l11IlI1I 													,													I1l1II11                              ,                             I1l11lll 												,												ll1I1ll1 														,														IlI1lII1                            ,                           lllIl1ll                       ,                      ll1lIIIl 												,												lIII1Il1 												,												lII11l1I 												,												III1IllI 								,								IIIl1l1l 											,											IIl1l11I 												,												l11I1Ill                   ,                  lll1111l 											,											I1IIII1I 																,																l1l1llI1                                ,                               l1lI1II1                            ,                           IIlIIII1 											,											llI1l11l 								,								I11Il111                          ,                         l1IllI1l                    ,                   lIIII1l1 									,									IlI111II                              ,                             IIIlI1I1                                ,                               I11lllI1 										,										llllI1l1 																,																I1lIIl1I 											,											I1IlIIlI                       ,                      lI1II11l 														,														IIIIIlII 									,									IIIl1lI1                             ,                            I1l1IIIl                                 ,                                lll1IIll 																,																lllI1111                    ,                   l1IlIIl1 									,									I11I1I11                   ,                  Ill1I11I 												,												Ill1lIl1 													,													Il1I1lI1                 ,                Illll1I1 														,														IllI1IIl                              ,                             lll1Il1I 														,														lIlI111I                         ,                        IlIl11Il                 ,                l1lll1II 																,																II1IIlll                                ,                               IlIlI111                  ,                 ll1l1II1                         ,                        l1l1l11I                              ,                             IlllllI1                           ,                          II1llIlI 										,										l1Ill1lI                   ,                  lIlI1111                           ,                          IIl1I1Il                    ,                   l1IllllI 										,										I11lI11l                       ,                      I1IIlIIl 										,										Il1lll1I 													,													l111l1II 													,													llIIlIl1 											,											l1I11lIl 													,													Illl1II1                   ,                  IlI11lIl 															,															I1Ill11I                                ,                               I1llllIl 														,														IllIlII1 																,																l1l1I1ll 								,								llll11II                                ,                               I1I1Il1l 											,											lI1Il11l                    ,                   l1I1lIll                           ,                          I1l1IllI                                ,                               ll1Ill1l                        ,                       l1l1ll1l 														,														lllIIlll 											,											II1lIIll                       ,                      I11IIlIl 											,											lll1lllI 											,											l1l1II1I 													,													IllI1l11                     ,                    llIIlI1I                            ,                           IIl11III                 ,                I1I1IlIl                             ,                            II1I11l1                            ,                           l11I1I1l                        ,                       lIIIl11l 											,											Il1llI11 										,										lI111lIl                           ,                          lII1II11 															,															l1IIl1ll                    ,                   l1I1l1lI                             ,                            IlIIlIl1 												,												I1II1II1 														,														IIIIIII1                          ,                         l1111Ill                   ,                  II1IlII1                            ,                           IlIllI1l 															,															Ill1I11l 														,														I111111l                           ,                          I1I1llI1 											,											IIl1I111                     ,                    IIllIl11 												,												l1II1II1                  ,                 II1l1lI1                 ,                I11l11ll 														,														ll11III1 								,								llIIIll1 															,															ll1l1I11                        ,                       IlIll1l1                           ,                          lIllIl11 												,												IIlIIlI1                  ,                 l11l1I11                       ,                      l111I1I1                              ,                             I1llI11I 								,								l1I1I11I 															,															lIl11III 														,														l1ll1III 									,									lllII1ll 															,															l1l1Il1l                                 ,                                ll11lllI                      ,                     Illl1III                 ,                l1IlI111 									,									Il1lIl1l 																,																ll1Il1II 																,																III1l1II                            ,                           l1Il11lI                        ,                       l1l111ll 										,										lIIII1ll 												,												llllI11I 														,														llIll111 																,																llI1Il1l                       ,                      IIIlIIlI                               ,                              I11I11lI                 ,                I111l1II                            ,                           l1II1ll1 									,									IIlllIll                      ,                     Ill1IIIl 										,										I111IIl1                             ,                            l1Il1l11                 ,                Il111lII                 ,                l1I1I1Il 															,															I1lIIIlI                                ,                               l11I1IlI 									,									llI1l1II                   ,                  I11ll1I1 										,										lll1l1ll 										,										IIl111I1 													,													IlII11Il                                ,                               Il111ll1 										,										II11lI1I 								,								llll1IlI                  ,                 ll1lI11l                      ,                     lIllIIll                       ,                      Il1l11I1 														,														I11lII11                  ,                 IIl1Il1l                           ,                          IlIIII1I                   ,                  IlI1111l 										,										I11lIIII 										,										lIl11llI                 ,                lIllllII                         ,                        IlIl1II1                             ,                            llI1II11                                ,                               IIl11I1I 													,													II1Ill11                                 ,                                l1lllIlI                               ,                              IlllIl11 															,															I1l1ll1I                    ,                   l1lI11Il 																,																IllllII1 														,														II1l11Il 												,												II1l11lI 													,													lI1l11lI                              ,                             IIlI11l1 												,												lIIIIIII                               ,                              II1IIIlI                   ,                  ll11lIlI                 ,                I1III1ll                    ,                   I1IllI1l 											,											II1IIIll 											,											l1II1llI 										,										lIll1I1l 											,											lI1Il1Il                                 ,                                I111lI1I 												,												Il1l1IlI 										,										IlIlllI1 											,											II1I1lIl 										,										II1llllI 								,								l1IllI1I 																,																l1lIlI1l                               ,                              lIIl1lII                     ,                    IIl1III1                      ,                     IlI1II1l                                ,                               l1IIlII1                  ,                 lIII111l                        ,                       llIlIIll 																,																ll1I11lI                    ,                   llllll11 									,									I1lIIl1l 											,											IlI1I1I1                              ,                             l1Il1llI 										,										III1ll1I                         ,                        Illl11II 									,									l1lI1IIl 													,													lI1ll11I                               ,                              IIlI1I11 									,									llIIl1II 												,												IIIlIlIl 											,											llI111ll 															,															II1I1l1I                             ,                            I111l11I                          ,                         IIllIIIl                         ,                        II11ll1l                                ,                               I1l1I1lI 										,										ll11I1Il                              ,                             IIIlll11 												,												lll1I1II                         ,                        IlIIIII1 															,															IIl1111I 									,									I11I111I 											,											II1I1111 													,													llIIIIIl 								,								Il1IIlII 									,									ll1Ill11                             ,                            llIIIIlI 								,								I1lllIl1 								,								lIlI1ll1 																,																I1I1l11l                        ,                       IIIIl1II                        ,                       ll1Il1lI 												,												IlllIIl1 											,											IlII1l11 										,										lIIlIl1l 												,												l1lI1I1I                       ,                      llI1IlIl                             ,                            lIII1lIl 													,													Ill111I1 																,																l1IIII1I 									,									llI1lIII 														,														IllIl11I                                ,                               lI11I11I                   ,                  Il1I111I 									,									IlI11llI 													,													IIl1II11                           ,                          Il1I1lll                        ,                       IIlllll1 												,												lIl1I1ll                  ,                 I1lI1I1I 								,								III1IIl1                          ,                         l1lIll1I                   ,                  l11lI1l1                      ,                     IllII1ll                         ,                        IIl11lll 															,															llIlIII1 												,												llIIIIll 																,																Il111IIl 								,								lIl11II1                          ,                         III1ll11 												,												l1IIIll1 								,								l11llI1I 																,																lI1IlIl1                             ,                            II1lI11I 									,									lIllllll                               ,                              II1III11                            ,                           lI1l1lI1 											,											l1I11IlI 													,													lIIIlI1l                     ,                    I1l1I111 																,																llIllIlI 									,									lll11111 												,												II1l1I1I                        ,                       l11lI1lI 								,								lIllll11                    ,                   l1llll1I                    ,                   l1111III                            ,                           IIlIIl1l                               ,                              IlIlllII                   ,                  llIIIIII 															,															IlIIlIll 										,										IIIl111I 										,										Il11llI1 														,														l1II1lI1                              ,                             l1lllllI                   ,                  l11Il1l1 											,											Illlll1l 								,								lIII1III 										,										I1I1lIlI 								,								II1lIIII 									,									IlI11ll1                               ,                              IllIIllI                              ,                             I1IlIII1 									,									llllIlI1                        ,                       IlllI1lI                                ,                               I1I11II1                  ,                 lll1llIl                       ,                      II11IllI 											,											I1l1lIll                    ,                   IIIII1l1                      ,                     lII1IlII                   ,                  l111I111 											,											Illl1I11                    ,                   Il1llII1                     ,                    I1IlIIll 								,								lI1IIIlI 													,													I111lIII 															,															lIIIl1lI 										,										I1111IlI 								)								                              =                              																(																'dnuos_hcnup/sdnuos/sr/stessa'                         [                                                :                       									:									                             -                             1                  ]                 								,								382580507 															^															558836922                                ^                               													~																											-														931306492 										,										                ~                                      (                      95696940                        -                       95697002 								)																					,													336767570 											^											893713279 																^																                     (                     798300771                                 ^                                247679817                                )                                                        ,                                                         (                                96486268 								^								105968633 								)								                      +                                                    -                              								(								356646534                 ^                382815987                            )                                                       ,                            899653266                      +                     														-														661413767                              ^                             													(													99429017 													^													199103926 								)								                            ,                            836343721 														+														                       -                       629378692 																-																                  (                  926493848 										^										997139841 												)												                       ,                                                     (                              450478320 												^												999484789                           )                          								-								                 (                 513375582                               -                              												-												45199357                             )                                                       ,                                                           (                                456858646                      ^                     789756661 													)													                            -                                                   (                       722562575                    -                   													-													152582321                  )                 													,													744217698                          ^                         16665264                             ^                                                           (                               543797948                    ^                   214705236                         )                        												,												codecs                                .                               decode                 (                b'72'										,										'hex'											)																									.														decode 										(										'utf-8'																)																											,											18289247 									-									                                -                                277499735                              ^                             															(															138727649 											^											434483580 												)																									,													                             ~                                                      -                         130527200                          -                                                    ~                                                       -                            130527168 											,											0.0 										,																										(																702148154 									^									841384951                                )                               															+															                     -                     										(										755215012                                 ^                                922535726                    )                   										,										                             ~                             														-														402808728 									^									                          (                          290124358                 ^                155758018                  )                                               ,                              str 												,												isinstance                 ,                													~																								-																								(													178464941 								^								178464930                               )                              								,								0.4                            ,                           '(3ceV'                   [                                                 :                                                            :                              																-																1                        ]                       														,														943226933 										-										867146357                      ^                                          (                     401999277 									^									327082049                    )                                                   ,                                663439623                          ^                         608139213 													^													                          (                          783029487 									^									756558345 											)											                ,                                      ~                      									-									                 ~                 																-																40 															,															0.1                   ,                  codecs 									.									decode 													(													b'596f75206172652064656164'									,									'hex'                              )                              															.															decode 										(										'utf-8'                      )                      															,															'2'															[															                  :                  									:									                     -                     1                        ]                       												,																										~																														-																54054266 														^														                                (                                222967376 														^														242416445 										)										                               ,                                                 (                  694147163                           ^                          837405661                   )                                                 +                               														-																										~																												-																414585687                      ,                     ''												.												join                              (                                                [                   chr                 (                lI1lIlI1 									^									42086                                )                               for lI1lIlI1 in                        [                       41991 																,																42005 															,															42005                              ,                             41987 												,												42002                               ,                              42005                       ,                      42057                  ,                 42004 													,													42005                        ,                       42057                             ,                            41993                      ,                     41988 													,													41996                                 ,                                41987                     ,                    41989                   ,                  42002                      ,                     42005 									,									42057                           ,                          41988 										,										41994 											,											41993                            ,                           41989 													,													41997                    ,                   42056 														,														41993 								,								41988 										,										41996                           ]                          													]																									)												                          ,                          559974716 									-									257135563 												^																										(														41910375 														^														276002069                       )                      														,														182734321                  +                 264555606 										^																								~																													-															447289952                   ,                  278631704 																+																602875180 											^											407446428                       -                      														-														474060477                        ,                       codecs 									.									decode 											(											b'2023204261736520426c6f636b20636c6173730a2020202020202020636c61737320426c6f636b28427574746f6e293a0a202020202020202020202020646566205f5f696e69745f5f2873656c662c20746578747572652c20706f736974696f6e3d28302c20302c2030292c20636f6f6c646f776e3d312e30293a0a20202020202020202020202020202020737570657228292e5f5f696e69745f5f280a2020202020202020202020202020202020202020706172656e743d7363656e652c0a2020202020202020202020202020202020202020706f736974696f6e3d706f736974696f6e2c0a20202020202020202020202020202020202020206d6f64656c3d276173736574732f72732f6f626a656374732f626c6f636b272c0a20202020202020202020202020202020202020206f726967696e5f793d302e352c0a2020202020202020202020202020202020202020746578747572653d746578747572652c0a2020202020202020202020202020202020202020636f6c6f723d636f6c6f722e636f6c6f7228302c20302c2072616e646f6d2e756e69666f726d28302e392c203129292c0a2020202020202020202020202020202020202020686967686c696768745f636f6c6f723d636f6c6f722e77686974652c0a20202020202020202020202020202020202020207363616c653d302e352c0a2020202020202020202020202020202020202020636f6c6c696465723d27626f78270a20202020202020202020202020202020290a2020202020202020202020202020202073656c662e626c6f636b5f74657874757265203d20746578747572650a2020202020202020202020202020202073656c662e69735f64657374726f796564203d206675636b5f75702846616c73652920202320466c616720746f20747261636b2069662074686520626c6f636b2069732064657374726f7965640a2020202020202020202020202020202073656c662e636f6f6c646f776e203d20636f6f6c646f776e2020232054696d6520696e207365636f6e647320726571756972656420746f20627265616b2074686520626c6f636b0a2020202020202020202020202020202073656c662e686f6c645f73746172745f74696d65203d204e6f6e652020232054696d65207768656e2074686520706c61796572207374617274656420686f6c64696e6720746865206c656674206d6f75736520627574746f6e0a2020202020202020202020202020202073656c662e686f6c64696e67203d206675636b5f75702846616c73652920202320466c616720746f20696e6469636174652069662074686520706c6179657220697320686f6c64696e6720746865206d6f75736520627574746f6e0a20202020202020202020202020202020616c6c5f626c6f636b732e617070656e642873656c66290a0a202020202020202020202020646566207570646174652873656c66293a0a2020202020202020202020202020202069662073656c662e686f6c64696e6720616e642073656c662e686f76657265643a0a202020202020202020202020202020202020202063757272656e745f74696d65203d2074696d652e74696d6528290a202020202020202020202020202020202020202069662063757272656e745f74696d65202d2073656c662e686f6c645f73746172745f74696d65203e3d2073656c662e636f6f6c646f776e3a0a20202020202020202020202020202020202020202020202073656c662e686f6c64696e67203d206675636b5f75702846616c73652920202320526573657420686f6c64696e672073746174650a20202020202020202020202020202020202020202020202073656c662e6f6e5f64657374726f7928290a20202020202020202020202020202020656c73653a0a202020202020202020202020202020202020202073656c662e686f6c64696e67203d206675636b5f75702846616c736529202023205265736574206966206e6f7420686f7665726564206f72206e6f7420686f6c64696e670a0a20202020202020202020202020202020676c6f62616c20707265765f706c617965725f706f736974696f6e0a20202020202020202020202020202020696620706c617965722e706f736974696f6e206973204e6f6e65206f722064697374616e636528706c617965722e706f736974696f6e2c20707265765f706c617965725f706f736974696f6e29203e20726566726573685f726174653a0a2020202020202020202020202020202020202020707265765f706c617965725f706f736974696f6e203d20706c617965722e706f736974696f6e0a2020202020202020202020202020202020202020666f7220626c6f636b20696e20616c6c5f626c6f636b733a0a20202020202020202020202020202020202020202020202064697374203d2064697374616e636528626c6f636b2e706f736974696f6e2c20706c617965722e706f736974696f6e290a20202020202020202020202020202020202020202020202069662064697374203c2072656e6465725f64697374616e63653a0a20202020202020202020202020202020202020202020202020202020696620626c6f636b2e706f736974696f6e20696e2064656163746976617465645f626c6f636b733a0a202020202020202020202020202020202020202020202020202020202020202064656163746976617465645f626c6f636b732e72656d6f766528626c6f636b2e706f736974696f6e290a20202020202020202020202020202020202020202020202020202020626c6f636b2e76697369626c65203d206675636b5f75702854727565290a20202020202020202020202020202020202020202020202020202020626c6f636b2e69676e6f7265203d206675636b5f75702846616c7365290a20202020202020202020202020202020202020202020202020202020626c6f636b2e656e61626c6564203d206675636b5f75702854727565290a202020202020202020202020202020202020202020202020656c73653a0a20202020202020202020202020202020202020202020202020202020696620626c6f636b2e706f736974696f6e206e6f7420696e2064656163746976617465645f626c6f636b733a0a202020202020202020202020202020202020202020202020202020202020202064656163746976617465645f626c6f636b732e617070656e6428626c6f636b2e706f736974696f6e290a20202020202020202020202020202020202020202020202020202020626c6f636b2e76697369626c65203d206675636b5f75702854727565290a20202020202020202020202020202020202020202020202020202020626c6f636b2e69676e6f7265203d206675636b5f75702854727565290a20202020202020202020202020202020202020202020202020202020626c6f636b2e656e61626c6564203d206675636b5f75702854727565290a0a20202020202020202020202064656620696e7075742873656c662c206b6579293a0a2020202020202020202020202020202069662073656c662e686f76657265643a0a20202020202020202020202020202020202020206966206b6579203d3d20277269676874206d6f75736520646f776e2720616e6420706c617965722e656e61626c65643a0a20202020202020202020202020202020202020202020202073656c662e706c61795f6372656174655f736f756e6428290a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20313a20626c6f636b5f74657874757265203d204772617373426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20323a20626c6f636b5f74657874757265203d2053746f6e65426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20333a20626c6f636b5f74657874757265203d20427269636b426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20343a20626c6f636b5f74657874757265203d2044697274426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20353a20626c6f636b5f74657874757265203d20426564726f636b426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20363a20626c6f636b5f74657874757265203d20476c617373426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20373a20626c6f636b5f74657874757265203d204261736963576f6f64426c6f636b0a202020202020202020202020202020202020202020202020696620626c6f636b5f7069636b203d3d20383a20626c6f636b5f74657874757265203d204261736963576f6f64426c6f636b506c616e6b730a202020202020202020202020202020202020202020202020626c6f636b5f7465787475726528706f736974696f6e203d2073656c662e706f736974696f6e202b206d6f7573652e6e6f726d616c290a0a2020202020202020202020202020202020202020656c6966206b6579203d3d20276c656674206d6f75736520646f776e2720616e6420706c617965722e656e61626c65643a0a2020202020202020202020202020202020202020202020202320537461727420686f6c64696e6720666f7220626c6f636b206465737472756374696f6e0a20202020202020202020202020202020202020202020202073656c662e686f6c645f73746172745f74696d65203d2074696d652e74696d6528290a20202020202020202020202020202020202020202020202073656c662e686f6c64696e67203d206675636b5f75702854727565290a2020202020202020202020202020202020202020656c6966206b6579203d3d20276c656674206d6f757365207570273a0a202020202020202020202020202020202020202020202020232053746f7020686f6c64696e672069662074686520627574746f6e2069732072656c65617365640a20202020202020202020202020202020202020202020202073656c662e686f6c64696e67203d206675636b5f75702846616c7365290a0a20202020202020202020202064656620706c61795f6372656174655f736f756e642873656c66293a0a2020202020202020202020202020202070756e63685f736f756e642e706c617928290a0a20202020202020202020202064656620706c61795f64657374726f795f736f756e642873656c66293a0a2020202020202020202020202020202070756e63685f736f756e642e706c617928290a0a202020202020202020202020646566206f6e5f64657374726f792873656c66293a0a202020202020202020202020202020206966206e6f742073656c662e69735f64657374726f7965643a0a202020202020202020202020202020202020202073656c662e706c61795f64657374726f795f736f756e6428290a202020202020202020202020202020202020202073656c662e69735f64657374726f796564203d206675636b5f75702854727565290a2020202020202020202020202020202020202020426c6f636b4974656d456e7469747928746578747572653d73656c662e746578747572652c206f726967696e616c5f626c6f636b3d747970652873656c66292c20706f736974696f6e3d73656c662e706f736974696f6e290a202020202020202020202020202020202020202064657374726f792873656c66290a2020202020202020202020202020202020202020616c6c5f626c6f636b732e72656d6f76652873656c662920'																,																'hex'																)																                     .                     decode 								(								'utf-8'													)																											,																											(													17555549 												^												898014891 															)																															-																															(															466448696                   +                  415239571 															)															                    ,                    9.8                              ,                                              ~                 												-																								(												674070716                        ^                       674070771                           )                          									,									''                           [                           														:														                            :                            												-												1                  ]                                         ,                        0.2 										,										31235963 											^											193828498                    ^                                        ~                                              -                         173083121 															,															codecs 													.													decode                               (                              b'706c616e65'                     ,                     'hex'                  )                                   .                 decode                     (                    'utf-8'                                )                                                     ,                     117453820 									^									342415647                 ^                                              ~                              										-										325642982 															,																													(														391887924 															^															329044264 														)														                              -                                                     (                       989410157 									^									1044274814 											)																					,										                   (                   934115471 												^												254328169                 )                                   -                   														~																														-																948291022                             ,                            364145371                   -                                         -                       379452215                        +                                            (                     237655852                     +                                                 -                             981253422                         )                        									,																	(								348549135 														^														998943807 																)																                  -                  											~											                             -                             793566203                                 ,                                'gnp.kcolb_ssalg/segami/sr/stessa'															[																							:								                                :                                                  -                  1                  ]                                          ,                         'kcolBssarG'                 [                 											:																										:															                   -                   1                  ]                 								,								                             ~                             											(											349868547 											+																						-											349868588                      )                     								,								"eid reven ll'I"													[																							:																							:													                   -                   1                                ]                               														,														''                       .                       join 								(								                [                chr                     (                    l1II11l1                      ^                     8465 								)								for l1II11l1 in 												[												8560                           ,                          8546                               ,                              8546                               ,                              8564 								,								8549                           ,                          8546 											,											8510                                ,                               8547 								,								8546                   ,                  8510                                 ,                                8568 													,													8572 												,												8560 									,									8566 										,										8564                                 ,                                8546                 ,                8510                                 ,                                8574 												,												8573 													,													8565                            ,                           8526 														,														8563                          ,                         8560 																,																8546 															,															8568                        ,                       8562 																,																8526 											,											8550 										,										8574 																,																8574 										,										8565 															,															8526                       ,                      8563                        ,                       8573 									,									8574                                ,                               8562 									,									8570 															,															8511 									,									8545 											,											8575                     ,                    8566 											]											                          ]                          										)																					,											315645145                   +                  490639754                             ^                            										(										548263104                     ^                    279132835 									)									                   ,                                   ~                								-								323461658 														-														                                ~                                                 -                 323461577                             ,                            'gnp.tols/segami/sr/stessa'										[																		:																				:												                       -                       1 											]											                             ,                             0.11 															,															''                            .                            join                    (                   											[											chr                                 (                                II1lII1l                                 ^                                13862                            )                           for II1lII1l in                             [                            13895                          ,                         13909 												,												13909                           ,                          13891 														,														13906                    ,                   13909                       ,                      13833                    ,                   13908                                 ,                                13909                                ,                               13833                             ,                            13903                              ,                             13899                    ,                   13895 										,										13889 									,									13891 												,												13909 									,									13833                     ,                    13891 																,																13908                              ,                             13908 											,											13897                               ,                              13908 															,															13945                             ,                            13890                    ,                   13891                 ,                13892                            ,                           13907 												,												13889 														,														13945                                ,                               13892 											,											13898                             ,                            13897                     ,                    13893 													,													13901 										,										13832 																,																13910                                ,                               13896                     ,                    13889 										]										                ]                                            )                                                            ,                                map 											,											273472368                               -                                                    -                      574204041                            ^                           																~																                           -                           847676412 													,													607136364 													-													                        -                        227300187                                ^                                                  ~                                          -                       834436561 											,											692968927                  +                 168510941 								-																					~													                           -                           861479835                                ,                               															~															                            -                                                         ~                                                  -                     11                                 ,                                ''								.								join                         (                                          [                  chr 															(															lIl111lI 														^														57038 													)													for lIl111lI in                          [                         56994 											,											57003 																,																57000 															,															57018                   ,                  57070                            ,                           56995 										,										56993 									,									57019 												,												57021 																,																57003                            ,                           57070 													,													57002                         ,                        56993                         ,                        57017 											,											56992                         ]                        									]																		)									                       ,                       type 										,										                             ~                             												(												842412473                          -                         842412507                     )                                                ,                            													~													                     (                     849816109 															-															849816127 									)									                  ,                                       (                     412058401                    ^                   200499704                 )                                 -                                               (                              90074622                            -                           									-									236876990                  )                 												,												''										.										join 													(																					[								chr                 (                l1IIIIII 										^										16098 																)																for l1IIIIII in 										[										16033                              ,                             16014                         ,                        16011                           ,                          16001                     ,                    16009                  ,                 16066 										,										16010                               ,                              16007 														,														16016                    ,                   16007 																,																16066                 ,                16022                           ,                          16013                       ,                      16066 														,														16019 									,									16023                   ,                  16011 											,											16022 																,																16066 													,													16022                            ,                           16010 													,													16007                        ,                       16066 								,								16005 									,									16003 														,														16015                 ,                16007 								]								                          ]                                          )                															,															247505374 								^								802118531                             ^                                                           (                               168911981                               ^                              723426838 													)													                        ,                                               ~                       													-																							(										948519095                                ^                               948519082 												)												                     ,                     									~									                   -                                       ~                    												-												45                                ,                                                             ~                              											-											762315003                    +                   															-																							(								94626564                          ^                         684975055                                )                                                 ,                  													~													                -                								(								39524559 															^															39524575                   )                  												,												codecs 																.																decode 													(													'nffrgf/ef/vzntrf/en2.cat'                        ,                        'rot13'                   )                   															,															858127190 										^										571889600 												^												                     (                     450323008 									^									199544512                    )                                                   ,                                14606774                      -                                            -                       953213363 												^												47688055                 -                                             -                             920132102                               ,                                                      ~                        												(												753860254 										-										753860258                           )                          									,									''                           .                           join 								(																				[												chr 										(										lIl111l1                            ^                           16800                        )                       for lIl111l1 in                               [                              16850                    ,                   16841 													,													16839                                ,                               16840                              ,                             16852                                 ,                                16768                                ,                               16845                                ,                               16847                  ,                 16853 											,											16851 													,													16837                    ,                   16768                          ,                         16836                    ,                   16847                       ,                      16855 										,										16846                                ]                                                          ]                           										)										                          ,                          									~									                             (                             212472691 											-											212472737                            )                           															,															codecs 								.								decode 													(													b'6173736574732f72732f736f756e64732f676c6173735f736f756e64'                           ,                           'hex'										)																									.															decode                        (                       'utf-8'												)																							,											codecs                   .                  decode 													(													'phor'											,											'rot13'                          )                                                       ,                             codecs                      .                     decode                     (                    b'6173736574732f72732f6f626a656374732f64656661756c745f6f626a2e6f626a'											,											'hex'								)								                      .                      decode                        (                       'utf-8'															)															                    ,                                            (                        121065734 										^										601297087                        )                                          +                   																-																																(																267148163 														^														722213607                    )                                          ,                       print 										,										                 (                 157271821 														^														273396322                          )                         								-																		(										183179408                             -                                             -                 237591761 															)															                              ,                              ''                              .                              join 												(																								[												chr                                 (                                lI111II1 										^										8356                   )                  for lI111II1 in 													[													8438                               ,                              8385                               ,                              8407                      ,                     8404                 ,                8389 												,												8403                       ,                      8394                            ]                                                  ]                                           )                                     ,                 574809016 											+											162287436 								^																	~									                  -                  737096488                                 ,                                0.5                          ,                         466944305 																-																														-														283363307 								+								                (                967193222                  -                 1717500746                  )                 														,																												~																												(														518362116                     +                                               -                           518362146 									)									                 ,                 0.1 													,													407673238                               ^                              36115025                              ^                                                     (                        770652353 											^											931443497 													)													                               ,                               								~																					-													157970148 										^										276846216                            +                                                           -                                118876098 								,																								~																											-											                (                870501805 																^																870501797 															)																									,																										~																												-												108649936                                 ^                                833148224 														-														724498262                    ,                   										(										636433368 								^								361671231                             )                                                -                                       (                   761691273                           ^                          487056700 									)																						,													358128431 												^												6447857                         ^                        364249888                            +                                                         -                              8063301 											,											'gnp.kcolb_ssalg/segami/sr/stessa'                          [                                                       :                             								:																						-														1                               ]                              																,																549805510 										^										22866476                      ^                                               (                          180226512 										^										724024861                   )                  								,								255704041                              ^                             323636056 								^								                (                602150610                  ^                 1066657378                              )                             															,															                     ~                                       -                  681769609                       -                                        (                  142444122 												^												551517243 															)															                       ,                       																(																980049347 													^													986477068                   )                                                  +                                                     -                                         (                    108942318                            ^                           114850905                                 )                                															,															744782259 								+																			-											104276912 								^								                               ~                                                         -                          640505347 									,																			~																							-													33372781                         +                                             -                                      (                 199787284 																^																169195845                    )                   								,								                    ~                                                    -                                228977117 												-																											(															244639177 									^									53546010                             )                            													,													346407082                                 +                                124827598                          ^                                                   (                          451943787                         ^                        115762482 										)										                      ,                      179286526                              -                                                    -                       780994860 													^																						~									                      -                      960281390 												,												554620048                            +                           74884855 											+											                       -                                        (                 533563385 													^													977861767 															)																								,									codecs 											.											decode 														(														b'6173736574732f72732f6f626a656374732f62675f6f626a2e6f626a'                             ,                             'hex'                       )                       													.													decode                                 (                                'utf-8'									)									                      ,                                                      ~                                                              -                              780455436                      -                                           (                      309647913                               -                                              -                470807511                              )                                              ,                 458837381 															-																														-															454536279                               ^                                                        ~                                              -                    913373686 																,																										~																		-								                             (                             586790945 																^																586790914                        )                       																,																916005816 															-															208099210 													^													199917613 										+										507988954 									,									0.6 											,											                       (                       126745664                              ^                             493320509                                 )                                														-																						~								                           -                           451577165                               ,                              365137809                       -                                               -                         362651304 															^																												(													565345972                   ^                  181620888                               )                              								,								''								[								                         :                                             :                                             -                         1                          ]                                            ,                   																~																											(											119006516                 +                                 -                 119006534                 )                                ,                561252642 											^											162014486                      ^                     											(											899506547 																^																490818894                                )                               								,								''								.								join 																(																															[															chr                       (                      lll1IIl1 									^									62574 											)											for lll1IIl1 in 													[													62479 										,										62493 													,													62493                                ,                               62475 													,													62490                             ,                            62493                    ,                   62529 												,												62492                  ,                 62493 													,													62529 									,									62471 											,											62467 									,									62479 								,								62473 																,																62475                       ,                      62493 									,									62529 														,														62476                  ,                 62492                   ,                  62471                               ,                              62477 													,													62469                       ,                      62513                        ,                       62476 													,													62466 									,									62465 									,									62477                         ,                        62469                              ,                             62528                  ,                 62494 															,															62464                           ,                          62473                 ]                										]																										)																                      ,                      codecs                          .                         decode 													(													b'2c'                       ,                       'hex'                   )                                          .                       decode                              (                             'utf-8'													)													                                ,                                                         ~                                                        -                               589164668                              -                             									(									472955898                           ^                          1059933107                   )                  												,												858027633 										^										92003844                            ^                           699488680 								+								212750037 															,															                          (                          650972685 											^											195888394 														)														                -                								(								29628305                 -                                            -                            731640651                     )                    											,											''											.											join 													(																											[														chr 										(										I1I11lIl                               ^                              5800 										)										for I1I11lIl in 										[										5789 															]															                ]                                       )                       											,																								(													797607883 												^												698213681 												)												                       -                                          ~                                          -                       102195933 												,												len 									,									'gnp.kcolb_enots/segami/sr/stessa'													[																									:																												:																									-									1                        ]                                           ,                    178713372 									-									                          -                          549251337                 +                								-								                   (                   666399833 								^								215722049                         )                                        ,                'gnp.kcolb_doow_cisab/segami/sr/stessa'                   [                                   :                									:									                 -                 1 															]																										,											dict                                 ,                                                      (                      165202064 														^														995237054 								)								                -                											(											204275040                               ^                              1051076977                   )                  												,												None                            ,                           835996823                         ^                        503677673                                 ^                                                              (                              701877208 											^											100926852 												)												                   ,                                                   (                                644478213 									^									930477483                             )                                             +                                           (                          220917765 														-														507965618 															)															                               ,                               										~																			(									150043456                        +                                                     -                              150043534 																)																                  ,                  565144877 												-												151536977                    +                   															-																															(																261020094                      ^                     388628089 										)																					,											'5'										[																									:																															:																                    -                    1 																]																                        ,                        645769108                                +                                                               -                                528246167                               ^                                                        (                          817672144                       ^                      935194225                         )                        																,																769374908 																^																798753798                               ^                              161306194                                 +                                												-												123049888 											,																									(														358039950                           ^                          288664602 															)															                 +                 												-																										(														606234229 												^												541166358 											)											                          ,                          'jbo.cm_jbo_tluafed/stcejbo/sr/stessa'											[																			:								                         :                                                     -                            1 															]																									,										codecs 										.										decode 									(									'dhnq'															,															'rot13'                       )                                          ,                   not 34                      ,                     327045581                            +                           313697092 													^																						(									547272126 													^													112083104                     )                                                   ,                               303053145 												^												855720137                               ^                                                   (                     759436401                            ^                           206925311                       )                                           ,                                               ~                                           -                 171470094 															+																												-													                          (                          603148506                  ^                 701185490 																)																                            ,                            									(									235644729 												^												278003447                        )                       														-																														(																956483225                           ^                          664313690                           )                          								,																								~																														-																									(											495190748 											^											495190745 								)																							,															                     ~                                      -                 870471430                 +                									-									                 (                 208352480 															^															1065968143                              )                             															,															0.1 											,											codecs                    .                   decode 												(												':'                            ,                            'rot13'													)													                            ,                            977449492 								^								459452622 																^																								(								777107933 															^															259111704                        )                       								,								842384718 																^																763109275 													^													175333862                  +                 349600022 																,																0.7                          ,                         ''														.														join 															(																												[													chr 													(													I1Illl1I 									^									31261 										)										for I1Illl1I in                 [                31347                    ,                   31346 														,														31343                   ,                  31344 									,									31356 												,												31345                         ]                                                      ]                                                )                                                 ,                               687671234                               +                                                      -                        494701763 												^												                            (                            269688312                        ^                       462645020                      )                     														,														''													.													join 								(								                            [                            chr                   (                  I1IlIIl1                     ^                    60510                    )                   for I1IlIIl1 in 														[														60479                             ,                            60461                  ,                 60461                      ,                     60475 										,										60458 								,								60461 									,									60529 																,																60460                              ,                             60461 								,								60529 								,								60465                             ,                            60476 																,																60468 													,													60475                                 ,                                60477 														,														60458 										,										60461                         ,                        60529 									,									60474 																,																60475                                ,                               60472                               ,                              60479                    ,                   60459 									,									60466 													,													60458 														,														60417 																,																60465                   ,                  60476 											,											60468                       ,                      60524                               ,                              60528 													,													60465                              ,                             60476                 ,                60468 													]													                  ]                                             )                                             ,                  										(										871406375 															^															498472072 																)																										+																			(									929121413                   +                                        -                      1705497631 												)																							,											115776821 									+									610559634                             -                                                  (                      483422764 									^									932934074 										)																		,								0.4 														,														164784677                               ^                              624754054 																^																97399080                        +                       656434793 														,														                      (                      675504857                   ^                  268555693                      )                     															-																											(												46773204 									-																			-										897123202 														)														                          ,                          445838114                              +                                                -                   321501996 																+																														-														                (                986732330                             ^                            1035559158 															)															                        ,                        															~															                               -                               192865912                      ^                     													(													973324246                            ^                           830298548 													)																											,														411507276 														^														387318864 												^																						(										698650814                             ^                            641044143 												)																				,								234513071 										^										289263194                            ^                                            (                 251595713                 ^                305702695                           )                                                          ,                                									~																						-													218630502                                 ^                                											(											10405145 													^													227986532                        )                       												,												438441854 															^															402058429 									^																									(																896201284 															^															951978410                   )                  																,																'nwod esuom thgir'                         [                         														:														                               :                               													-													1                   ]                  										,																			(									550520359                            ^                           827042954                        )                                                  -                           																(																326232876                             ^                            48890240 								)								                           ,                           												(												76182814 										^										760181698                       )                      																+																																-																                         (                         537841243                 ^                164350156                      )                                               ,                          'sknalPkcolBdooWcisaB'								[																							:																											:																									-													1 											]											                             ,                             												~												                           -                           699345947 									^									846053701 												-												146707692 														,														434420313                         +                                                      -                              17181961 										+																									-																															(																339914552                   ^                  211558925 									)									                               ,                                                   (                    850126736 															^															484890503 															)															                   +                                           (                        707502493                                -                               1484313006                   )                                               ,                             ''                              .                              join 										(																						[												chr 									(									l1ll1111                                ^                               54291 															)															for l1ll1111 in                     [                    54352                       ,                      54399                        ,                       54394 										,										54384 														,														54392 									,									54323                      ,                     54395                          ,                         54390 														,														54369 											,											54390                          ,                         54323                    ,                   54375 																,																54396                             ,                            54323                          ,                         54370                   ,                  54374 														,														54394                         ,                        54375 													,													54323 													,													54375                         ,                        54395                       ,                      54390                         ,                        54323                         ,                        54388 														,														54386 											,											54398 																,																54390 								]																		]										                                )                                									,									290352608                         ^                        1071140844                     ^                    625491636 																-																																-																156099458 								,								'1'                              [                                                      :                                                     :                             												-												1 												]												                  ,                  codecs 								.								decode 															(															b'206c6f61645f776f726c645f70726f636573733a546872656164203d20546872656164287461726765743d6c6f61645f776f726c642c20617267733d2222290a20202020202020206c6f61645f776f726c645f70726f636573732e7374617274282920'									,									'hex'                  )                  											.											decode 													(													'utf-8'										)										                      ,                                       ~                                      (                     643611226 															+															                       -                       643611235 													)													                            ,                            ''                  .                  join                        (                                                      [                               chr                      (                     lIllIlII                             ^                            14531                            )                           for lIllIlII in 															[															14581 												]																											]															                            )                            																,																''                           .                           join 																(																											[											chr                             (                            I1ll111I                              ^                             10633                       )                      for I1ll111I in                                 [                                10749                     ,                    10732 									,									10737 															,															10749 																]																                                ]                                                      )                      												,												0.05                    ,                   4280007 												-																						-										173765719                                +                               											(											243726517                              -                             421772170                              )                                                  ,                                       ~                  										-										                (                218611779                  ^                 218611786                              )                             											,											codecs                  .                 decode 														(														' qrs hcqngr(frys):\n                tybony ceri_cynlre_cbfvgvba\n                vs cynlre.cbfvgvba vf Abar be qvfgnapr(cynlre.cbfvgvba, ceri_cynlre_cbfvgvba) > erserfu_engr:\n                    ceri_cynlre_cbfvgvba = cynlre.cbfvgvba\n                    qvfg = qvfgnapr(frys.cbfvgvba, cynlre.cbfvgvba)\n                    vs qvfg < eraqre_qvfgnapr:\n                        vs abg frys.vf_ernpunoyr:\n                            frys.vf_ernpunoyr = shpx_hc(Gehr)\n                            frys.uvtuyvtug_pbybe = pbybe.juvgr\n                    ryfr:\n                        vs frys.vf_ernpunoyr:\n                            frys.vf_ernpunoyr = shpx_hc(Snyfr)\n                            frys.uvtuyvtug_pbybe = pbybe.oynpx '								,								'rot13'                             )                                                ,                   															~																															-																                           ~                           												-												45                                ,                               'nwapser ot ereh kcilC'									[									                        :                                          :                  														-														1 												]																					,									codecs                                 .                                decode                      (                     'nffrgf/ef/bowrpgf/oybpx.bow'                     ,                     'rot13'											)																											,																                            ~                            								(								753191663                      -                     753191711                    )                   								,								812973604 											-																											-																78976809                          -                         														(														413767883 									^									763596273                   )                                      ,                    0.5                              ,                             ' )eurT(pu_kcuf = erongi.kcolb                            \nkcalb.roloc = roloc_thgilhgih.kcolb                                \n)eslaF(pu_kcuf = elbahcaer_si.kcolb                                \n:elbahcaer_si.kcolb fi                            \n:esle                        \n)eslaF(pu_kcuf = erongi.kcolb                            \netihw.roloc = roloc_thgilhgih.kcolb                                \n)eurT(pu_kcuf = elbahcaer_si.kcolb                                \n:elbahcaer_si.kcolb ton fi                            \n:ecnatsid_redner < tsid fi                        \n)noitisop.reyalp ,noitisop.kcolb(ecnatsid = tsid                        \n:skcolb_lla ni kcolb rof                    \nnoitisop.reyalp = noitisop_reyalp_verp                    \n:etar_hserfer > )noitisop_reyalp_verp ,noitisop.reyalp(ecnatsid ro enoN si noitisop.reyalp fi                \nnoitisop_reyalp_verp labolg                \n:)fles(etadpu fed '                           [                                                    :                         														:														                  -                  1 														]																													,															''                    .                    join                         (                                           [                   chr                              (                             Il1I1I11 											^											22106                                )                               for Il1I1I11 in                            [                           22124                    ]                   										]																						)																										,														codecs                        .                       decode 										(										'j'                   ,                   'rot13'															)																									,																							(													265888175                  ^                 404043785 									)																						-													                     (                     585179030                           -                          185927159                              )                                                         ,                            378061924                    +                   81907060                     ^                                    (                280485117 														^														199052549                          )                         										,										0.18                          ,                         894400188                                ^                               771175768                        ^                       											(											614692168                                ^                               1008416416                              )                             									,									0.01                                 ,                                                         ~                         														-																											(													201144013 														^														201144021                        )                       								,								''                         .                         join 									(									                            [                            chr 								(								IlIl11I1                             ^                            25847                     )                    for IlIl11I1 in 												[												25747                            ,                           25758                    ,                   25750                               ,                              25754 										,										25752                    ,                   25753                                 ,                                25747 									]									                ]                										)										                    ,                                                  ~                                                  -                                       (                   836743615 											^											836743242                     )                                    ,                317268011                       +                      110634871 									+									                              -                              											~											                       -                       427902860                               ,                              249026841                        ^                       85617564 										^																							(													875001958 										^										1072351992                        )                                                 ,                          964743227 											^											233725878 									^									668524537                              -                                             -                211136436 														,														codecs 												.												decode 														(														b'4261736963576f6f64426c6f636b'														,														'hex'															)															                        .                        decode                      (                     'utf-8'                             )                             										,										                      ~                                                 -                                                    (                         690774118                       ^                      690774115                    )                                          ,                       344269494                              -                             255652147 														^																										~																							-											88617350                                 ,                                17                          !=                         74 								,								754492863 												-												434831408                      +                     														-														                        (                        589988791 															^															807872059                          )                                                   ,                                                      ~                                                          (                              266801796                               -                              266801847 									)																	,								892773321 															-																														-															56174036 														^														                  ~                                      -                    948947331 														,														'dnomaid'                          [                          															:																													:														                     -                     1 														]														                     ,                     ''                          .                          join 																(																										[										chr                         (                        l1II1I11                 ^                38836                      )                     for l1II1I11 in                    [                   38797 											]																									]														                   )                   											,											793337876                                ^                               547228475 														^														937733763                               +                                                              -                                671957844                               ,                              codecs                          .                         decode 										(										b'6173736574732f72732f696d616765732f707963725f6c6f676f2e706e67'									,									'hex'																)																                              .                              decode                                 (                                'utf-8'															)																											,												29085229 														-														                 -                 596477559                                -                               												(												172290527                  ^                 789423445                             )                            									,									' )(dlrow_daol                \n)dlrow_tluafed(seniletirw.)"w" ,)emandlrow(tamrof.\'wcp.dlrow/}{\'(nepo                \n)"r" ,\'wcp.dlrow/tluafed/sdlrow\'(nepo = dlrow_tluafed                \n)"...gnitteser dlrow gntrats"(tnirp '                              [                                                :                  												:												                 -                 1 											]											                 ,                 93942753                              ^                             42289884                    ^                   235937416                 -                116647271                             ,                            854811869 									+																							-														714970329 											+											                         (                         536953624                             +                            													-													676795132 														)														                             ,                             													(													642578640 											^											671837032                        )                                        +                 									(									704896429                               +                                               -                 944468301 															)															                ,                														~														                   -                   335683779 												^												                         (                         602094334 															^															937499174                         )                                         ,                 														~														                        -                        955407127                                +                               									-									                        (                        51028654                         ^                        1006172230                                )                                                         ,                          0.95 											,											                             ~                             													-																								(											924598055                            ^                           924598075 												)												                           ,                           bool                                 ,                                0.9 												,												                 ~                                 -                381956464                        -                       															~																														-															381956458 											,											''													.													join                         (                                          [                  chr 																(																llIllIIl 													^													17100                     )                    for llIllIIl in 														[														17069 												,												17087 									,									17087                       ,                      17065 									,									17080                                 ,                                17087                           ,                          17123 										,										17086                     ,                    17087 																,																17123 															,															17061                 ,                17057                                 ,                                17069                              ,                             17067                     ,                    17065                   ,                  17087 											,											17123                             ,                            17086 										,										17069                          ]                         									]									                    )                                        ,                    118527469                   ^                  407382785                               ^                              									~																					-												525909751                          ,                         84540211                       +                      60988821                        ^                       597732058 								+								                       -                       452202992                         ,                        'erehpsoci'								[								                        :                                                    :                            												-												1 									]									                   ,                   352858036                      +                     382751606                                ^                               219395985                  +                 516213641 									,									212760489                        -                                       -                777264146                 ^                                ~                											-											990024586 												,												codecs 								.								decode                      (                     'nffrgf/ef/vzntrf/onfvp_jbbq_oybpx.cat'											,											'rot13'										)										                      ,                      13 									==									13                       ,                      502339984                       ^                      994348698 												^												122655114 									-									                      -                      526779777                          ,                         474023679 										^										608193427 															^															741342648 													-																										-													198266813                     ,                    913033563                           +                                                -                      260000756                            ^                           480773840 											+											172258929 									,																			(										790555295                    ^                   478366879                            )                                            +                                               -                                                          (                            615758322 									^									388897793 																)																                         ,                                                     ~                            												-												694411147                          ^                                              (                     318801793 																^																979589127 								)								                              ,                              441988413                       -                      39867420 														^																										~																										-														402120967 								,								codecs                    .                   decode                   (                  b'6173736574732f72732f696d616765732f61726d5f746578747572652e706e67'                    ,                    'hex'                         )                         											.											decode 								(								'utf-8'															)															                              ,                              837915099 													-													337591155 									+																							(														273212770 												-												773536708                            )                           										,										0.0005                       ,                      609735947                               ^                              342833543 													^													671619180                            +                           137417792 										,										codecs 										.										decode                     (                    b'6173736574732f72732f696d616765732f646972745f626c6f636b2e706e67'										,										'hex'                               )                               												.												decode 														(														'utf-8'                    )                                      ,                  											~											                        (                        997475579                      -                     997475609 													)													                         ,                         codecs                       .                      decode                    (                   'dhnq'                  ,                  'rot13'                              )                                                          ,                            399970859                                +                               249673788 											-											                              (                              990133472 								-								340488874                                 )                                									,									46656593 															-																															-																45979185 								^								                    ~                                              -                          92635813 								,								codecs                     .                    decode                     (                    'OrqebpxOybpx'                             ,                             'rot13'                )                                         ,                         ''								.								join                           (                                                 [                       chr                            (                           lllll11l 																^																53769 																)																for lllll11l in                 [                53886 												,												53856 																,																53883 												,												53868 									,									53871                             ,                            53883 															,															53864                           ,                          53860                            ,                           53868                   ,                  53846 											,											53866 												,												53884 													,													53867 												,												53868                 ]                											]											                       )                       								,								226589127 															+															363178758 									^																						(													981737112 															^															430127708 										)										                   ,                   													(													115608618                      ^                     803955667                       )                                       -                                  (                 70473033                       +                      618404451 								)																					,																											(														912519942                      ^                     556939317 												)																				+																		-																						(												812781042                      ^                     656656102                          )                         												,												''												.												join 											(																					[										chr                           (                          I11lI1ll 								^								22438                   )                  for I11lI1ll in 											[											22471                 ,                22485                   ,                  22485                         ,                        22467                         ,                        22482 									,									22485 															,															22409                  ,                 22484 														,														22485 												,												22409 														,														22473 								,								22468 																,																22476                             ,                            22467 													,													22469 								,								22482 															,															22485                         ,                        22409                         ,                        22471 										,										22484                        ,                       22475                   ,                  22408 												,												22473                     ,                    22468 									,									22476 																]																											]																								)													                                ,                                                  (                  370769503 												^												20956204 														)																													+																											-												                  ~                  														-														388414001 													,													591475937 														^														244666834 												^												                               (                               106586554 												^												730727567 														)														                               ,                               								(								662115651                   ^                  365003355                      )                                              +                         											-											                            ~                                                            -                                850826993                            ,                           454082882                         ^                        590687684                         ^                        339705815 									+									602303711 									,									int 										,																					(											800814561                          ^                         978397791 											)											                         +                                                -                                                (                         40656279                             ^                            394658536                          )                                                      ,                             461835351                                +                               19262921 											-											                      (                      147912844                  +                 333185423                        )                       																,																codecs                            .                           decode 									(									b''										,										'hex'                                )                                								.								decode 														(														'utf-8'                      )                      													,													'.dlrow ruoy ni dnuof ton wcp.dlrow'								[								                    :                                              :                          								-								1 												]												                   ,                   890560860 															+																														-															763591802 												^												                      (                      533030347                  ^                 408158479                               )                                              ,                166138136                                 ^                                501686539 									^									703523216                    +                                             -                          367966583 								,								'dlrow gnivas dehsiniF'								[								                           :                                                  :                                                -                         1                                 ]                                											,											692530623 									+									41511188 									-									                  (                  948193191                       ^                      323277279 								)																		,										codecs                 .                decode 												(												'Fnir Jbeyq'                           ,                           'rot13'									)																		,									codecs                          .                         decode 															(															'nffrgf/ef/vzntrf/fxlobk_qnl.cat'                      ,                      'rot13'								)																					,													537218622 															-															170497424                            ^                           736318473                         -                        369597318                         ,                                        ~                                   -                   										(										134257237                              ^                             134257223 															)															                           ,                           22                               <                              9 									,									838991980                      +                                      -                 162308642                          +                                            -                                        ~                                               -                          676683285 											,											938210001                     +                    														-														660022487                      +                     																-																                    (                    567609997                 ^                826394485 													)													                             ,                             0.15 											,											291382524 										^										909661395                                 ^                                                 (                 506142870                              ^                             961368237                   )                  													,																													~																                    -                    68011291                    ^                   											(											336115974                                 ^                                268794898                              )                                                       ,                          bool                    (                   47                                 )                                                 ,                 enumerate                 ,                'emag eht ot nruter ot ereh kcilC'														[																								:																				:																						-												1                               ]                              																,																                   ~                                   -                810810272                     ^                    551373362                            +                           259436934                     ,                                       (                   845733397 								^								883824944 															)															                     +                     																-																											~																											-																113689806                            ,                           codecs                    .                   decode 										(										b'6c656674206d6f75736520646f776e'                          ,                          'hex'                    )                    														.														decode 											(											'utf-8'												)																					,									674082515 											^											1018137436                          ^                         767600592 													-													423526915 														,																													~																											(												8942738                       +                      															-															8942788 												)												                              ,                                                            ~                              											(											611128125                      +                                          -                     611128172 															)																													,														177076560                              +                             512452967 											-																			~																					-													689529454                     ,                    bool 										(										38                         )                        															,															223735933 																+																353809939 															+															                -                                  (                  25497496                              ^                             602515741                 )                                         ,                         727280267 															^															220252458                    ^                   87263622 												-																							-											558242307                      ,                     319766966 															+															                          -                          242256069                           ^                          											(											589917992 											^											666359755                 )                                      ,                      267351872                    ^                   622332156 												^																				(								87802897 								^								801946557                            )                           										,																					~											                     -                                           ~                      												-												28                         ,                        																~																                 -                                      (                     598229818                                ^                               598229817 												)																					,									codecs 									.									decode 												(												b'6173736574732f72732f6f626a656374732f626c6f636b'								,								'hex'                         )                                            .                   decode                              (                             'utf-8'                 )                 									,									codecs                           .                          decode 													(													'3'                  ,                  'rot13'                        )                                             ,                     ''																.																join 											(											                                [                                chr                          (                         lIlll1ll                                ^                               12378                              )                             for lIlll1ll in                          [                         12344                  ,                 12341 											,											12322 									]									                    ]                    																)																                   ,                   898538351 																^																944562528 								^								709743373 										+																				-										478894303 																,																														~														                 (                 556748227 										+																					-											556748272 																)																															,															767685500 												^												999630248                  ^                 												~												                  -                  374658791 										,										405922526 															^															503164064                         ^                        												(												16019153                             ^                            87564469                              )                             											,																						~											                           (                           655765383                     -                    655765564                 )                											,											367038563 											+											                    -                    225831241                   +                                             -                                                    (                         8817681                      ^                     149695233 														)																							,									codecs                               .                              decode                    (                   'fcurer'												,												'rot13'								)								                           ,                                             (                  452774389 											^											237308917 														)																											+																					-								                           (                           851111085                              ^                             644033807                           )                                                  ,                        717025858 																+																										-										532993511                 ^                                               (                               933447712                  ^                 1029395556 														)																						,								codecs                               .                              decode 												(												'nffrgf/ef/vzntrf/en.cat'													,													'rot13'                                )                                										,										range 															,															993211865                    -                   203330269                    ^                   												(												959033803 															^															373101363                       )                      														,																														~																								(								389545065                  +                                    -                   389545083                     )                    															,															0.0                             ,                            478132012                                 +                                448793810                    -                                               ~                            															-															926925805 												,												codecs 								.								decode                            (                           'nffrgf/ef/vzntrf/jngre_oybpx.cat'                      ,                      'rot13'                               )                                                       ,                        open                      ,                     0.07 														,														915338417                             -                            844542383                     ^                    785931229                    +                   													-													715135170 													,													codecs 											.											decode 														(														b'737068657265'								,								'hex'															)															                          .                          decode                  (                 'utf-8'										)										                         ,                         568039656 														+														118097693 									-																						(													658513576                             ^                            262504794 								)																		,										766501709 												^												988367509 													^													                    (                    443711010 														^														221566933 											)																											,																                (                195074578 								^								184870398                        )                       											+											                                -                                                 (                 244151458 												^												237570930                    )                   													,																						(									264104474 										^										472583361                   )                                                +                                                          -                            											(											512941281 																^																218380953                                 )                                										,										codecs                   .                  decode 										(										b'37'															,															'hex'											)																				.									decode 														(														'utf-8'                )                                         ,                                                  ~                                                   -                          															(															879303275                               ^                              879303272                  )                 													,													607829170                    ^                   578879314                           ^                          									(									740725728 												^												714919964 																)																												,												210560521                                 +                                595705864 								-																					(													948928444 											^											142727773 																)																								,								'b'									[																									:																                              :                                                 -                   1 								]																,																			(											715173469                                ^                               903248415                              )                             											+																				(									487112956 													+													                              -                              1014994158 								)								                           ,                           'kcolBtriD'                     [                                                   :                                                        :                                                   -                         1                           ]                                                  ,                        																~																                -                								(								877945889 											^											877945860                 )                											,											                               ~                               														-																						(								838007240                              ^                             838007259 										)										                               ,                               15708429                 +                473168572                                ^                               															(															504049418                           ^                          52987111 												)																										,																											~																								-																								(													617483527 										^										617483600 													)																					,								codecs 										.										decode 														(														'{}/jbeyq.cpj'                             ,                             'rot13'												)																				,								743082413                         -                        															-															157736313 												^												                      (                      541162952 																^																368057032                  )                 																,																''										.										join                 (                																[																chr                      (                     IIlI1III 												^												30867 														)														for IIlI1III in                  [                 30906 												]												                            ]                            								)																,								str 									,									codecs                       .                      decode 									(									b'504155534544'                    ,                    'hex'                               )                                                               .                                decode                               (                              'utf-8'                          )                                                   ,                         								~																							-															868304609                             +                                               (                   635424695 									-									1503729232 														)														                               ,                               297899522                        ^                       645541601                             ^                            869806402                             -                                              -                  65243019                              ,                             162447823                    ^                   811558800                              ^                                                          (                             83439294 																^																1023969529                 )                															,															0.07 														,																						~																						-														                 (                 97945602                            ^                           97945629 									)																								,															0.15 															,															                         ~                         													-													                         ~                                              -                     42                    ,                   'jbo_tluafed/stcejbo/sr/stessa'                                [                                																:																									:																					-												1 															]																													,														259205543                            -                                                      -                           602374555                             ^                                                       ~                                                      -                           861580097                   ,                  985137702 												+																						-										99632361 								^								849574351                        -                       								-								35930959                       ,                      906407042                          ^                         218304693                             ^                            													(													281116021 													^													734314817 												)												                       ,                       codecs 																.																decode                             (                            '8'													,													'rot13'                 )                                 ,                355401226                             ^                            603585864                           ^                          613129353 										+										306931427 										,										                               (                               882797444 										^										501368607 										)										                                +                                														(														447268096                   +                  																-																1143271798                            )                           															,															217231686                            ^                           195390672                              ^                             195812361                     -                    72613503                         ,                        																~																                    -                    946075232 												+																											-															                       (                       102942000                       ^                      1044460384                                )                                                  ,                   746346478 													^													537975121 																^																										~																										-																208441069 								,								                          (                          496442399 															^															913445089                 )                                  -                                             (                           718006556                    ^                   19850612                         )                                                    ,                            581230108                               -                              											-											21520817 												^												725940394 												-												123189481 															,															                               (                               179415861 										^										202353929                   )                                    +                                      -                                              (                          38969973 											^											82617437 													)													                            ,                            316658134 																+																576647984 											+											                                -                                															(															916825484                             ^                            60514676 								)								                     ,                     codecs                       .                      decode 											(											b'6c656674206d6f75736520646f776e'										,										'hex'															)															                           .                           decode                         (                        'utf-8'                            )                                                    ,                        15754665 												+												559057537                     ^                    282396839                       -                      												-												292415363                  ,                 748924745 										-																						-												198916393 														^														21847420 									-									                         -                         925993710                                ,                               56763342                                ^                               782058350 														^														                            (                            583189158 																^																255697419                         )                                             ,                     														~																											-													578997024 														^																						(								805870928                               ^                              311055948                  )                                       ,                                            ~                                       (                 604042233                           -                          604042256 													)																												,																								~																						-																										(													138250540 													^													138250528                          )                                                      ,                             831358792                               -                              503661307                      -                     									(									839755033                            +                           											-											512057561                          )                                             ,                    387905823                         ^                        495151267                    ^                   61323513 													+													116775098 															,																							~																							(															752658745 													-													752658788 																)																                   ,                   0.07 								,								codecs                    .                   decode 												(												b'436c69636b206865726520746f207361766520776f726c64'								,								'hex'														)																								.										decode                               (                              'utf-8'                              )                              												,												0.1                            ,                           ''													.													join                                 (                                                [                chr                               (                              l1lIlllI                          ^                         49455 									)									for l1lIlllI in 											[											49486 															,															49500 													,													49500                  ,                 49482                    ,                   49499                  ,                 49500                       ,                      49408 									,									49501                        ,                       49500 												,												49408                               ,                              49478                          ,                         49474                            ,                           49486 																,																49480 														,														49482                             ,                            49500 												,												49408                           ,                          49483                 ,                49482                                 ,                                49485 									,									49498                        ,                       49480                      ,                     49520                              ,                             49485 												,												49475 													,													49472 										,										49484 										,										49476 														,														49409 												,												49503                                ,                               49473                             ,                            49480                               ]                                                           ]                             										)																							,													codecs 																.																decode                  (                 'obk'                    ,                    'rot13'                        )                        								,								                        ~                        													-													                      (                      12454982 									^									12455016 													)																					,								209163388 													+													                              -                              55914411                           ^                          											(											874185901 														^														1027170416                 )                									,									                         ~                         													(													446421262 											-											446421311 																)																                         ,                         								~								                     -                     937723711 												-												                 ~                                    -                   937723663 											,																										~															                          -                                                  (                        655513495 													^													655513519 									)									                              ,                              705899376                           +                          27099111 																-																								(								166881833 															^															574800145 											)																									,																						(								221976969 									^									143125305                       )                                                    -                              															~																												-													96268973 											,											393952196 														+														                       -                       238994366                  +                                               (                              968287741                               +                              										-										1123245535 												)																										,														                               ~                                                     (                      793238160 													+																													-																793238243 										)																								,														codecs 														.														decode                                (                               'rfpncr'                                ,                                'rot13'												)												                ,                																~																															-															                                (                                281920223                          ^                         281920199                   )                                              ,                                             (                 428190108 												^												1062339016                                 )                                                  +                  														(														78345864 														+																										-												730013400                                 )                                															,															'kcolBenotS'														[														                      :                      													:													                       -                       1 															]																															,																													~																						-									465860504                               -                                                            (                              687644457                             -                            221783987 								)								                            ,                            91157269 															^															23809239 															^															                 (                 332024797 													^													399504393 																)																										,										                          ~                                                          -                                241322327                          ^                                          (                 286336881 												^												527658496                    )                                              ,                                                      ~                                               -                    												~																									-													48                           ,                                            (                  85253273                          ^                         695482228                     )                                                   -                               								~								                   -                   744549340                  ,                 244988689                      +                     106885737 														+																											-													                                (                                598206224 												^												928959061                                 )                                															,																										(											187218137                        ^                       1030319976 																)																                   +                   																(																889511367                               +                              									-									1799796058 																)																                       ,                       														~																						-								933092041 															+																														-																													(														211412270                              ^                             990134246 								)								                            ,                            507781840 												-																								-												388690041                  ^                 437151727                                -                               														-														459320174 									,									0.5 															,															700170727                         +                        275700884 													-																					~																							-															975871579                             ,                            472642992 													+																												-															28977701                         +                        																-																												(												610827563                       ^                      1041872459                            )                           																,																codecs 									.									decode 												(												'nffrgf/ef/vzntrf/en2.cat'											,											'rot13'										)																				,										630812089                              ^                             1068589652 												^												                (                87065807                            ^                           521702183 									)									                 ,                 222603603                               ^                              642442391 												^												194658658 											-																			-								527699061 								,								0.0                     ,                    832781129 													+													                 -                 76981914 													^																													(																731634179 														^														110579333                        )                                          ,                   											~																					-										                               (                               529418053                    ^                   529418077 														)														                               ,                               																~																                            -                            								(								492103311 												^												492103325                 )                                ,                														~																													-																									(										755984261 										^										755984278 															)															                ,                698736591                    +                   286390274                      ^                     																(																271028059                              ^                             714102948                                 )                                										,										                            ~                                                -                    379471951                              ^                             254578725 													+													124893247                          ,                         not 23                     ,                    ''                             .                             join 															(															                     [                     chr 								(								llIIIlI1 										^										43838                   )                  for llIIIlI1 in                             [                            43900                          ,                         43852 															,															43863 													,													43869 								,								43861 												,												43900                        ,                       43858                        ,                       43857                            ,                           43869                   ,                  43861                    ]                   								]																)								                       ,                       codecs                      .                     decode                   (                  b'6173736574732f72732f6f626a656374732f626c6f636b2e6f626a'                          ,                          'hex'                )                                 .                 decode                            (                           'utf-8'                        )                        													,																											(														323674234 								^								259375264 													)													                      +                                                 (                           276429811                 +                														-														750329006 															)															                             ,                             																(																214735353 										^										1041227883                             )                            								-								                   ~                                                   -                                851671350                        ,                       															~															                 -                 549279894 											^																							~												                               -                               549279891 								,								                   ~                   															-															202341932                     ^                    15636471                               +                              186705455                                 ,                                'gnp.thgin_xobyks/segami/sr/stessa'                       [                                            :                     									:									                                -                                1                   ]                  											,											492438925 										-										333291457 								-								                            ~                                                       -                           159147425                  ,                 staticmethod                                ,                               13                   >                  38                             ,                            0.1 											,											''													.													join                          (                                                 [                        chr 															(															llI1I1ll                  ^                 41235 														)														for llI1I1ll in 										[										41330 								,								41312 										,										41312                         ,                        41334                    ,                   41319 													,													41312                                ,                               41276                    ,                   41313                             ,                            41312                    ,                   41276                   ,                  41312                               ,                              41340                                ,                               41318                  ,                 41341 															,															41335                              ,                             41312 															,															41276                     ,                    41329                      ,                     41340 														,														41312                 ,                41312 												,												41250 													,													41292                       ,                      41312                                 ,                                41340                                 ,                                41318 									,									41341 									,									41335                       ]                      															]															                                )                                                    ,                    													(													431028732                  ^                 902407330                    )                                               -                            										(										177396492 														^														652969480                    )                   															,															codecs                               .                              decode 													(													'nffrgf/ef/vzntrf/phefbe.cat'														,														'rot13'											)											                     ,                     														~																						-								381477673                 ^                											~											                             -                             381477669 															,																											~																								-												750441448                            +                                                       -                                                 ~                                                -                           750441414 													,													587533835 									^									634780204                    ^                                                 (                              744067206                 ^                713647248                    )                   														,																						~								                 -                                             (                            414097206 																^																414097275                               )                                                           ,                             945844588                          ^                         298555746 															^																													~														                        -                        699131957 										,										679375058 															^															454506801                 ^                964520426 												+																						-										101982197                     ,                    ''														.														join 															(															                            [                            chr                     (                    IIIlll1I 										^										51540                              )                             for IIIlll1I in 								[								51494                           ,                          51517                           ,                          51507                            ,                           51516                      ,                     51488                          ,                         51572 									,									51513                    ,                   51515 															,															51489                         ,                        51495                              ,                             51505 																,																51572                            ,                           51504                          ,                         51515                     ,                    51491 												,												51514 										]										                             ]                             														)																									,											codecs                           .                          decode                                 (                                'nffrgf/ef/vzntrf/fxlobk_qnl.cat'                           ,                           'rot13'                )                												,												87346948 												+												324135924                               ^                                              (                310970803 										^										168801093                       )                                              ,                        													~													                      -                      642408354 										+										                      -                      										~																						-												642408339 									,									261685509 														-														                -                344253393                 ^                														(														133046618 											^											603178393 												)												                        ,                        '4'                              [                                              :                                            :                            												-												1 														]																											,													440507970                                +                               48697144 																^																899527998                              -                             410322917 														,														645462091                    ^                   762485727 								^								                        (                        588148478 										^										671354228                   )                  															,															bool 														(														21 																)																                       ,                                        ~                 								(								291798433 									+																							-														291798478 									)																							,														792316160 										+										25996546                                +                               									(									404141308                 -                1222453977 													)																						,									120815035 															^															869693377 									^																						(													965316238                              ^                             225215696                             )                                               ,                   														~														                      -                      514843114                   +                  											(											945913913 									+																				-											1460756952 														)														                             ,                             codecs                          .                         decode 															(															b'6173736574732f72732f696d616765732f67726173735f626c6f636b2e706e67'                            ,                            'hex'                             )                             												.												decode                         (                        'utf-8'											)											                              ,                              														~																										-																					(									807435084 									^									807435111                         )                                           ,                   419466072 																+																117381123                         ^                                                   (                           47255457                              ^                             489598127                   )                                           ,                                         ~                								(								119672482                                 +                                												-												119672519 								)																			,											188226655 														+														29822146                             +                            														(														489573821 														-														707622617                           )                          																,																													~													                          (                          240810057                   -                  240810093 											)																				,									'gnp.kcolb_sknalp_doow_cisab/segami/sr/stessa'                        [                        									:									                        :                        								-								1                           ]                                                  ,                        155213290 									-									                  -                  482140866 													+													                     -                     													(													679646895                       ^                      226481674 									)									                ,                'pot_vu_ebuc'                [                											:																			:								                  -                  1 											]																					,																				~										                 -                 642601686                 ^                												(												410373838                         ^                        1043897422 															)															                      ,                      464173316 															-															                          -                          28017763                             ^                            858554785                               -                              366363683                         ,                        codecs 										.										decode 										(										b'6173736574732f72732f696d616765732f72612e706e67'                ,                'hex'                  )                                             .                           decode                  (                 'utf-8'                        )                        																,																''                  .                  join                                 (                                															[															chr                              (                             I1l1l111 																^																15692                    )                   for I1l1l111 in 								[								15617                          ,                         15661                               ,                              15653 								,								15650                 ,                15724 														,														15617                        ,                       15657 													,													15650 											,											15673 													]																						]																									)																                           ,                                            ~                                             -                                                      (                          956694663                          ^                         956694734                             )                            															,															codecs                        .                       decode                         (                        b'2e2e2f2e2e2f2e2e2f6173736574732f72732f7575682f68656c6c6f2e747874'								,								'hex'                  )                  								.								decode 												(												'utf-8'										)										                          ,                                                 (                       175358936 										^										173068660                              )                                                  -                                                    ~                               									-									2298496                  ,                 												~												                                -                                791055246                                -                                                             (                              815984940                               ^                              528775759                               )                              								,								283039014 															+															526319206                               -                                              (                757079369                     ^                    488492564                   )                  								,																					~																						-									                            (                            231615006                           ^                          231614987 													)													                             ,                             codecs 												.												decode 																(																b'51756974205468652047616d65'														,														'hex'                   )                   										.										decode                  (                 'utf-8'											)											                      ,                      ''									.									join                             (                            											[											chr 														(														llIlIlIl 								^								28069                     )                    for llIlIlIl in 															[															28100                               ,                              28118                           ,                          28118                   ,                  28096 									,									28113                         ,                        28118 												,												28042                                 ,                                28119 												,												28118 											,											28042                    ,                   28108                             ,                            28104                         ,                        28100                                 ,                                28098                        ,                       28096 								,								28118                             ,                            28042                              ,                             28103 									,									28096                  ,                 28097                                 ,                                28119                   ,                  28106                             ,                            28102 											,											28110                            ,                           28154                             ,                            28103                              ,                             28105 													,													28106 														,														28102 											,											28110 																,																28043 																,																28117                        ,                       28107                           ,                          28098                           ]                          										]																		)								                         ,                         36                    !=                   36 													,													'gnp.kcolb_gubed/segami/sr/stessa'                            [                                                :                    								:								                    -                    1                     ]                                               ,                           0.11                          ,                         555489312                      +                                           -                      448235852 																^																348328075                    +                                              -                           241074699                            ,                           176173708 														-														                              -                              195253873                                +                                                         -                          										~										                -                371427572 										,										'gnp.kcolb_sknalp_doow_cisab/segami/sr/stessa'                  [                  													:																												:															                   -                   1                              ]                             										,										                                (                                188878129 									^									166234965                              )                             										+										                      -                      														~														                        -                        44729918                   ,                  383134901 														^														630863968                      ^                                                (                           836880424                           ^                          44948702 											)																						,											967105058                        ^                       1038541782 													^													                         (                         140254987 								^								203302627 											)											                             ,                             ''                      .                      join 											(											                 [                 chr                 (                lII1l1l1 								^								32016 									)									for lII1l1l1 in 											[											32098 													]													                                ]                                                )                                      ,                      ''								.								join 										(																										[																chr                     (                    lIIll1l1 												^												22466                   )                  for lIIll1l1 in                               [                              22405 								,								22446                    ,                   22435 												,												22449 													,													22449                          ,                         22400                                ,                               22446                        ,                       22445 									,									22433                            ,                           22441                              ]                             														]																													)																								,									                  (                  857017891                  ^                 186648032 															)																								-																				(											639051576 											^											505556097 															)																										,											732441783 										^										167301788 											^											239610888                            +                           336122410 															,															583223547 								^								869248025 												^												                              (                              148258720 											^											433773377 												)												                            ,                            ''                             .                             join                               (                              											[											chr                       (                      lIIIIlIl                         ^                        61579                    )                   for lIIIIlIl in                          [                         61669 																,																61668                              ,                             61689                               ,                              61670                                ,                               61674                     ,                    61671                   ]                  								]																)																		,																		(								923942863 															^															256846894 								)								                               -                                                     (                      393802338 													^													791011798 													)													                          ,                          												~												                      (                      681059743 												-												681059762 										)																										,																codecs                          .                         decode 																(																b'6173736574732f72732f696d616765732f70616f6c6f672e706e67'									,									'hex'													)																									.												decode 										(										'utf-8'															)																														,															764677297 															^															959371026 													^													                               ~                                                      -                       347790244                          ,                                             ~                                     -                 500974852 														^														824045245 											-											323070385 									,									395564600 												^												477991591 									^									985571383 														+																						-								785406845 																,																0.05 									,									                                ~                                																-																923074517 														^														601616395 										-										                      -                      321458161 												,												181261948 									^									860342835 										^																						~												                -                965352539 													,													codecs                          .                         decode 															(															'Dhvg Gur Tnzr'                        ,                        'rot13'                           )                           									,									154250776 										^										596888316 												^												745421184 															-															30135446                      ,                     										~										                             -                             283661395                          +                         										(										861454470 																+																															-															1145115823 																)																                              ,                              628500222                 -                456228440 												^																											~															                   -                   172271791                                ,                               ''                    .                    join                 (                																[																chr                            (                           IlIlIIl1                        ^                       5748 															)															for IlIlIIl1 in 															[															5639 																,																5663                       ,                      5645 								,								5675 										,										5648 									,									5659                 ,                5657                              ,                             5649                      ]                                                    ]                               										)																						,												not 36                 ,                codecs                        .                       decode 								(								'8'                            ,                            'rot13'                        )                        											,											                     ~                     												(												674493791 																-																674493809                               )                              																,																'k'                               [                                                :                                 :                                           -                           1 																]																																,																                  (                  532123541                           ^                          181615832 												)																										-																												(														541504141                            ^                           891421089                  )                                                 ,                                											(											654379329                               ^                              651543526                 )                                        +                        								(								200555052 													-													231277684                      )                                     ,                codecs 												.												decode 											(											b'6173736574732f72732f696d616765732f62617369635f776f6f645f706c616e6b735f626c6f636b2e706e67'														,														'hex'                           )                           													.													decode                         (                        'utf-8'								)								                            ,                            															~															                             -                             503552282                               +                              													-													                (                450783815 														^														81654610                                )                               													,													2.75 																,																'gnp.rosruc/segami/sr/stessa'                         [                                               :                      															:															                                -                                1                       ]                                                     ,                                                 (                  334319619                                 ^                                579878104                         )                        								+								                           -                                                      (                           337429676                             ^                            627157117                    )                                             ,                          codecs 													.													decode 													(													b'776972656672616d655f71756164'                           ,                           'hex'                        )                        													.													decode                      (                     'utf-8'																)																                          ,                          codecs 													.													decode                 (                b'737068657265'                               ,                               'hex'								)								                        .                        decode                       (                      'utf-8'                      )                                             ,                       0.4                              ,                                                       ~                                                       (                             66463359 										-										66463365 															)																							,								31                 ==                31                    ,                   								~								                               -                               135673254 															+																														-																							(								204520542                     ^                    69634321 													)													                           ,                           399643427 									+									                 -                 42534700                  -                 												(												508657963 														^														186157820 									)																								,															'emaG ehT ot nruteR'                 [                                 :                													:													                         -                         1                           ]                                                     ,                                            ~                                           -                          252509321 								^																		(										115166713                            ^                           164737401 								)								                              ,                              														~																											-													                       (                       796844465                            ^                           796844442                            )                                                          ,                                                 (                  300779093 											^											639309490                 )                											-											                  ~                                                -                              938905791 													,																										(													871471791 												^												571664936 								)																						-														                   (                   257952895 													^													511927020 								)																,																							~																													(														898358156 									-									898358168                   )                  											,											455067988                                +                               286565139 												+																											(															909176771 															+																							-								1650809896 										)										                      ,                      																(																396757506 														^														175041148 															)															                        +                        															(															730663525 								-								1230367362 													)																									,												tuple 													,																						~									                            -                            81661955                   -                                               ~                             										-										81661939                           ,                          165791428                     -                    159205587 									^									103843260 																+																														-														97257430                           ,                          1.5 								,																						~														                       (                       847267688 														-														847267736                            )                           								,																			~																								-																								~																						-											2 																,																883081007 										^										349888750 											^											                         (                         439758411                        ^                       978219466                       )                      														,														0.5 									,									75537637 											-																										-															486445366                               ^                              108049452                      +                     453933556                            ,                           630323095                             ^                            985971641                 ^                															~																														-															525683719 														,														277697338 									^									638966299 												^																							(											776487045                       ^                      416336275                                )                               									,									                              ~                              											-											145928470 								-																			~																										-															145928441                            ,                           isinstance 								,								codecs 																.																decode                               (                              'pvepyr'								,								'rot13'                      )                      															,																									(										419515242 													^													49375774 															)																												-													                        (                        922949554 																+																                           -                           454227519                     )                                                ,                            898488769 												+												                    -                    341379631 															^																								(									296530289 																^																815300339 																)																																,																''									.									join                        (                                                 [                          chr                                 (                                ll11111l 									^									33877 									)									for ll11111l in 														[														33847 												]												                             ]                                               )                  																,																																(																465269440                              ^                             685026781                              )                                                   +                      									-																	(								358554484                     ^                    640730540                               )                                                              ,                                216529330                             ^                            579180449                         ^                                                        (                                695864638 												^												119038759 														)																						,								'gnp.kcolb_doow_cisab_dlo/segami/sr/stessa'                [                                          :                          											:																											-																1                         ]                                        ,                0.7 														,																							(									101574140                       ^                      740523216                      )                                                +                           																-																                           (                           410421229                           ^                          844635892                         )                                            ,                    666385980                            ^                           231913147                             ^                                                ~                    														-														711624845 													,													codecs                           .                          decode 										(										b'20646566207570646174652873656c66293a0a2020202020202020202020202020202073656c662e69735f726561636861626c65203d2064697374616e63652873656c662e706f736974696f6e2c20706c617965722e706f736974696f6e29203c2072656e6465725f64697374616e63650a2020202020202020202020202020202073656c662e686967686c696768745f636f6c6f72203d20636f6c6f722e77686974652069662073656c662e69735f726561636861626c6520656c736520636f6c6f722e626c61636b20'                            ,                            'hex'												)												                .                decode                     (                    'utf-8'															)															                 ,                 																(																902846196 											^											28122573 													)																											+														                          -                                            (                  578818560 									^									385702174 									)																									,																'llik/sdnuos/sr/stessa'														[														                      :                                             :                       														-														1                              ]                                                 ,                                                 ~                                                -                   												~												                        -                        18                   ,                  925276611 												-												692674119                   +                                               (                             588852903                               +                              								-								821455358 												)												                              ,                                                       ~                                                       (                              943214139                 +                										-										943214162                     )                                        ,                                               ~                           																(																664339766 														+														                        -                        664339829 														)																													,															208460040 													-													                           -                           701225743 																-																                     ~                     								-								909685750 										,										codecs 										.										decode                      (                     ' qrs hcqngr(frys):\n                tybony ceri_cynlre_cbfvgvba\n                vs cynlre.cbfvgvba vf Abar be qvfgnapr(cynlre.cbfvgvba, ceri_cynlre_cbfvgvba) > erserfu_engr:\n                    ceri_cynlre_cbfvgvba = cynlre.cbfvgvba\n                    qvfg = qvfgnapr(frys.cbfvgvba, cynlre.cbfvgvba)\n                    vs qvfg < eraqre_qvfgnapr:\n                        vs abg frys.vf_ernpunoyr:\n                            frys.vf_ernpunoyr = shpx_hc(Gehr)\n                            frys.uvtuyvtug_pbybe = pbybe.juvgr\n                    ryfr:\n                        vs frys.vf_ernpunoyr:\n                            frys.vf_ernpunoyr = shpx_hc(Snyfr)\n                            frys.uvtuyvtug_pbybe = pbybe.oynpx '                       ,                       'rot13'                           )                           											,											415540619 												^												1025610911                 ^                										(										755569879                       ^                      149693935 																)																														)														










def l1111l1l 									(									I1IllIl1 														)														                      :                      








                    return True 







def l1I1IllI                      (                     I1IllIl1                           )                          															:															




                    return I1IllIl1 



I1llll11                            =                           lambda IIl11lII 								:								True 




llllI1Il 										=										lambda IIl11lII                     :                    IIl11lII 










class Il11lIll 												:												




                    @																staticmethod 




                    def llIl11II 											(											IlII1lll                              )                             																:																



                                        return True 





                    @                          staticmethod 


                    def Il11l1I1 									(									IlII1lll 												)												                    :                    









                                        return IlII1lll 





def llllIIII 										(										Illl11l1                       ,                      IIlllIlI 								)																					:													






                    try 																:																




                                        return Illl11l1                          >=                         IIlllIlI 








                    except 											:											







                                        return not Illl11l1 											<											IIlllIlI 









def IIII11lI 											(											I1ll11I1                        ,                       IIlIIlII                      )                     									:									








                    try 									:									



                                        return I1ll11I1 										!=										IIlIIlII 



                    except 																:																





                                        return not I1ll11I1                           ==                          IIlIIlII 








def lIl1I11I                               (                              l11lIIlI                        ,                       ll1llI11                    )                                                   :                                

                    try 								:								
                                        return l11lIIlI                       ==                      ll1llI11 







                    except                         :                        




                                        return not l11lIIlI                           !=                          ll1llI11 









def ll1I11II                    (                   IIlllI1I                       ,                      l11lI1I1                              )                             									:									




                    try 								:								


                                        return IIlllI1I 															>															l11lI1I1 







                    except 												:												









                                        return not IIlllI1I                            <=                           l11lI1I1 








def IlIIII1l                                (                               lI1I1ll1                       ,                      II1I1l11                          )                         															:															



                    try                 :                









                                        return lI1I1ll1 								<=								II1I1l11 
                    except 									:									







                                        return not lI1I1ll1                   >                  II1I1l11 





def lI11I1l1 								(								lll1III1 										,										IIll1Ill                      )                     															:															


                    try 																:																




                                        return lll1III1                              <                             IIll1Ill 


                    except 												:												




                                        return not lll1III1 															>=															IIll1Ill 




bossEnabled 											:											Il1Il1I1 														=														llllIlIl 





def llIlll11                    (                   l11I1Il1                                 )                                														:														








                    l11IlI1l 																=																I1I1IlIl 







                    lIl1lI1I 													=													lI1l11lI 







                    if not Il111IIl 									:									
                                        lIl1lI1I                         =                        II11IlIl 





                    else 														:														








                                        lIl1lI1I 															=															lIIll1II 








                    if lIl1lI1I 																==																IIIllI1I                                 :                                




                                        if not bossEnabled 												:												


                                                            lIl1lI1I 									=									lll11IIl 



                                        else                   :                  




                                                            lIl1lI1I 														=														II11IlIl 




                    if lIl1lI1I 									==									II11IlIl 								:								



                                        l11IlI1l 																=																lI11llll 






                    if lIl1lI1I 																==																lll11IIl 								:								





                                        l11IlI1l                    =                   I111l111 








                    if l11IlI1l 											==											lIII1III                           :                          
                                        llI1l11I                          =                         l11l1lII 



                                        if not l1111l1l 													(													llllIlIl 										)										                :                


                                                            llI1l11I                     =                    ll1Il1II 








                                        else                                :                               









                                                            llI1l11I 													=													II1IIIll 

                                        if llI1l11I 													==													llI1Il1l 										:										

                                                            if not l1111l1l 										(										I11I111I 									)																				:											









                                                                                llI1l11I                     =                    ll11I1Il 



                                                            else 											:											







                                                                                llI1l11I                                =                               I1l1IllI 

                                        if llI1l11I                 ==                ll1Il1II 																:																
                                                            l11IlI1l                             =                            lI11llll 









                                        if llI1l11I                                 ==                                Ill1lI1l                                :                               




                                                            l11IlI1l                   =                  I1l1II1l 
                    if l11IlI1l 								==								l1I11IlI                            :                           







                                        return l11I1Il1 
                    if l11IlI1l 															==															II1l1lI1                           :                          





                                        pass 









                    IlI11III                       =                      lll1IIll 

                    l11IlIl1 													=													l1l1IIIl 



                    if not ll11I1Il 								:								



                                        l11IlIl1 																=																l1IIllI1 
                    else 															:															





                                        l11IlIl1 														=														l11I1Ill 







                    if l11IlIl1                    ==                   Il1I111I                              :                             

                                        if not lI1l11lI 															:															









                                                            l11IlIl1                    =                   III1111l 





                                        else                       :                      

                                                            l11IlIl1                         =                        llll11II 






                    if l11IlIl1                      ==                     l1IIllI1 																:																








                                        IlI11III                   =                  l1l1IlIl 



                    if l11IlIl1 															==															llll11II 															:															









                                        IlI11III                            =                           l1ll1Il1 


                    if IlI11III                        ==                       l1ll1Il1 												:												

                                        lI1IIlIl 								=								l1IIllI1 


                                        if llllIIII                           (                          random                 .                random 														(														                        )                        										,										IIllIlIl 											)											                          :                          





                                                            lI1IIlIl                          =                         llIlIIll 



                                        else 										:										



                                                            lI1IIlIl 											=											Il11llll 


                                        if lI1IIlIl 														==														Il11llll                           :                          



                                                            if not I1llll11                      (                     IllIlII1                         )                        													:													


                                                                                lI1IIlIl 															=															llIlIIll 

                                                            else                      :                     

                                                                                lI1IIlIl                              =                             l1I11II1 




                                        if lI1IIlIl 															==															l1I11II1 									:									









                                                            IlI11III                        =                       ll1lIIIl 


                                        if lI1IIlIl                                ==                               lIlIlIll 												:												



                                                            IlI11III 																=																IIl11lll 






                    if IlI11III                 ==                IIl11lll                      :                     








                                        pass 






                    if IlI11III 																==																Il111l1I                     :                    









                                        return l11I1Il1 


                    return not l11I1Il1 








def fuck_up                   (                  value                    )                   											:											



                    return llIlll11                              (                             value                            )                           

def l1IlI1II                           (                          l11IIll1 															)																											:												





                    Ill1lII1 											=											llI1IlIl 








                    lIIIlI1I 														=														lIlI11I1 


                    if not I1llll11 											(											II11111I 									)																		:									


                                        lIIIlI1I 												=												l1IIl1ll 




                    else                        :                       





                                        lIIIlI1I 											=											IIIll1Il 









                    if lIIIlI1I 														==														II1I11ll 															:															



                                        if not IIII11lI                          (                         Il111lII                           ,                          lIllllll 															)																											:												




                                                            lIIIlI1I 								=								llIII1lI 

                                        else                    :                   







                                                            lIIIlI1I                                =                               IlIIl1ll 






                    if lIIIlI1I                  ==                 IlIIl1ll 								:								
                                        Ill1lII1 													=													IllIlI1l 





                    if lIIIlI1I 									==									IIIll1Il                        :                       


                                        Ill1lII1                                 =                                l11I1IlI 








                    if Ill1lII1 																==																l11I1IlI                                :                               







                                        l1Il1II1                      =                     llI1IlIl 







                                        if not bossEnabled                    :                   









                                                            l1Il1II1                      =                     l1I1lIlI 








                                        else                     :                    





                                                            l1Il1II1                                =                               IllIll1l 


                                        if l1Il1II1 												==												IllIll1l                               :                              

                                                            if not Il11lIll 															.															llIl11II                            (                           l11l1lII 										)										                      :                      

                                                                                l1Il1II1                         =                        Il1lIlI1 






                                                            else 																:																





                                                                                l1Il1II1                         =                        lII11l1I 



                                        if l1Il1II1                        ==                       lII11l1I                     :                    







                                                            Ill1lII1                     =                    II1IlII1 




                                        if l1Il1II1 																==																I1llI11I                     :                    









                                                            Ill1lII1 																=																lI1Il1ll 




                    if Ill1lII1 										==										IIII1IlI                 :                



                                        pass 









                    if Ill1lII1 															==															IIIlIIlI 																:																




                                        return l11IIll1 







                    l1l1l1lI 														=														lll1l1ll 

                    l1lllll1                               =                              l11l11l1 
                    if not IlI11ll1                     :                    

                                        l1lllll1                          =                         lIIl1lI1 

                    else                 :                








                                        l1lllll1 									=									l111l1II 



                    if l1lllll1                             ==                            l111l1II 											:											





                                        if lIl1I11I                         (                        l11IIll1                     ,                    ll1l11II                   )                                  :                




                                                            l1lllll1 									=									IIl1l11I 





                                        else                     :                    








                                                            l1lllll1                      =                     IIlI1I11 





                    if l1lllll1 																==																l1llIll1                       :                      





                                        l1l1l1lI                       =                      IllllII1 








                    if l1lllll1 														==														IIl1l11I 															:															


                                        l1l1l1lI 									=									IIlIl1I1 








                    if l1l1l1lI 														==														IIlI1I11                            :                           
                                        I1Ill1II 															=															l1llll1I 








                                        if lIl1I11I 													(													lI1llI11 												,												IllllII1                 )                                          :                          




                                                            I1Ill1II                     =                    Ill11llI 






                                        else 														:														




                                                            I1Ill1II                       =                      lll11IIl 
                                        if I1Ill1II 								==								I11lI11l                         :                        






                                                            if not Il11lIll 													.													llIl11II                      (                     llII1llI                             )                                                  :                      


                                                                                I1Ill1II 														=														Ill1I11l 









                                                            else 															:															




                                                                                I1Ill1II                            =                           II11IllI 






                                        if I1Ill1II                             ==                            lll11IIl                              :                             
                                                            l1l1l1lI 								=								lIlI1II1 






                                        if I1Ill1II                             ==                            I111II1I 											:											


                                                            l1l1l1lI                     =                    llI111ll 




                    if l1l1l1lI 									==									IlI1ll1l                    :                   






                                        return random 														.														random                       (                                       )                 															*															l111l1II                           *                          l11IIll1 








                    if l1l1l1lI 															==															Il1IllIl 														:														





                                        return random                     .                    random                       (                                            )                      





def fuck_up_i                        (                       value                     )                                             :                         







                    return l1IlI1II                       (                      value 												)												




def I1I1Il1I                          (                         lllIIlIl                           ,                          lIIIIll1                     ,                    II1111I1 																,																IllIlIl1                            )                           																:																



                    lIIIIll1                              .                             menu_manager 								=								IllIlIl1 



                    lIIIIll1                          .                         menu_manager 											.											stop 																(																															)															




                    global player 









                    global boss1_sound 







                    player                         =                        Player 									(									username                   =                  lllIIlIl 										)										


                    lIlI1Ill 									=									player                               .                              position 


                    l1I111ll                                 =                                load_texture                       (                      II1I1lIl 										)										









                    II1IIll1                   =                  load_texture                    (                   II1l11lI                 )                






                    Il1IIIlI 														=														Audio 													(													lIll1II1                         ,                        loop 															=															fuck_up 																(																I11I111I                             )                                                         ,                             autoplay                  =                 fuck_up                         (                        I1IlIIlI 												)												                      )                      






                    II1111lI                           =                          Audio 								(								lIIlll1l                              ,                             loop 											=											fuck_up                       (                      llllIlIl                                )                               															,															autoplay                                =                               fuck_up                    (                   I11I111I                                )                                                           )                            







                    boss1_sound                       =                      Audio                       (                      ll11lIlI 														,														loop 									=									I1IlIIlI                                ,                               autoplay 															=															llllIlIl 								)								









                    boss1_sound                                .                               play                               (                              									)									






                    IIllIllI                      =                     Audio                                 (                                l111I111                  ,                 loop 								=								lIIIIIII                           ,                          autoplay                         =                        fuck_up 								(								I1IlIIlI 									)																					)												

                    global block_pick 






                    block_pick 												=												fuck_up_i                    (                   l1l1IIIl                            )                           


                    I1ll1IIl                    =                   II1IIll1 









                    global escmenuenabled 
                    escmenuenabled 								=								fuck_up 										(										lIIIIIII                      )                     









                    global isplayerkilled 
                    isplayerkilled                  =                 fuck_up                     (                    III1IIl1 												)												









                    global cameraposition 







                    cameraposition                      =                     l1lI1I1I 



                    II1llIll 										=										fuck_up_i 										(										lllIII1l                         )                        







                    lIIIlI11                   =                  II1111I1 






                    global textures 

                    textures 															=															                      [                      IllI1l1I                        ,                       lI1ll111 										,										llIIIIlI                                ,                               IIl1111I                   ,                  ll1111l1                                ,                               I1IllI1l 										,										lIIII1ll                                 ,                                llII1l1l 															,															II1l1lII                                ,                               lIIIIlII 								,								I1lIIl1l 														,														Il11IlIl 											,											Ill111I1                          ,                         II1IlI1l                     ,                    II1I1l1I                           ,                          I11lII11 														,														I11lllI1 													,													II1l11lI 												,												lllIIIll                 ,                lI1lI1I1 															,															I1I1Il1l                        ]                       







                    global objects 
                    objects                             =                            										[										III1IllI 								,								III11Il1 								,								IlllIl11 								,								lI1II1Il                    ,                   I11l1II1 														,														I1II11l1 										,										lI1lIlIl                               ,                              lllIl1ll 										,										ll11IlII                  ,                 II1lIIII                  ,                 I1I1IlII 									,									l11llI1I 																,																lI1IlIl1                     ,                    lIl1l1lI                        ,                       lI1Ill11 															,															llIIl1II                           ,                          I1lI1I1I 														]														


                    def hardcore_go_back 								(																					)																							:										



                                        lIIIIll1                                 .                                menu_manager 								.								go_back                          (                                                  )                         



                    def go_back                              (                             												)												                           :                           




                                        for ll1IIlI1 in I1Ill11I 												(												l1IIIll1 											)											                              :                              



                                                            llIllIII                      =                     l111I11l 




                                                            lIIll1ll 											=											IIl11II1 






                                                            if not I1llll11 										(										I1I11IIl                          )                                               :                      









                                                                                lIIll1ll 															=															l1llIIIl 
                                                            else                          :                         







                                                                                lIIll1ll                          =                         lllI1l1l 
                                                            if lIIll1ll 										==										lllI1l1l                              :                             







                                                                                IlIIl11l                    =                   IlIlIll1 






                                                                                II1I1llI 											=											lI1Il1ll 






                                                                                lI1l11Il 								=								lllII1ll 




                                                                                if not lIllllll 											:											
                                                                                                    lI1l11Il                               =                              I11I11lI 





                                                                                else                    :                   






                                                                                                    lI1l11Il 											=											IIll1I1I 









                                                                                if lI1l11Il                  ==                 I1l1llII                    :                   







                                                                                                    if not l1l1IlIl                     :                    








                                                                                                                        lI1l11Il 																=																III1111l 





                                                                                                    else 															:															








                                                                                                                        lI1l11Il 																=																lI1Il1ll 


                                                                                if lI1l11Il 									==									I1lllIIl 											:											
                                                                                                    II1I1llI 													=													lllII1ll 



                                                                                if lI1l11Il 															==															l1IllI1I 												:												





                                                                                                    II1I1llI                          =                         llI11llI 
                                                                                if II1I1llI                     ==                    lllII1ll 											:											



                                                                                                    I1I111Il 								=								lI1IlI11 





                                                                                                    if not II1l1Il1                            :                           



                                                                                                                        I1I111Il 													=													I1IllllI 





                                                                                                    else                            :                           

                                                                                                                        I1I111Il 												=												Il11l111 







                                                                                                    if I1I111Il                       ==                      I1IlIIll                                 :                                



                                                                                                                        if not l1111l1l                  (                 IlIll1l1 														)														                                :                                






                                                                                                                                            I1I111Il                         =                        II11IIlI 








                                                                                                                        else                  :                 





                                                                                                                                            I1I111Il 										=										I1IllllI 



                                                                                                    if I1I111Il                   ==                  l1l1IIIl                     :                    









                                                                                                                        II1I1llI 											=											llI11llI 





                                                                                                    if I1I111Il 																==																l1llllI1                              :                             
                                                                                                                        II1I1llI                                =                               Ill111l1 


                                                                                if II1I1llI 															==															llI11llI 										:										



                                                                                                    IlIIl11l                               =                              I1l1IllI 



                                                                                if II1I1llI                               ==                              IIlIlIlI 												:												







                                                                                                    IlIIl11l 														=														lIII1Il1 



                                                                                if IlIIl11l                       ==                      IIl1I1ll 										:										



                                                                                                    IllllI1I                               =                              Ill111l1 


                                                                                                    IIIll1lI                                 =                                Ill1IIIl 



                                                                                                    if not IIII11lI                            (                           I11lI11l 								,								ll1II1ll                       )                      										:										




                                                                                                                        IIIll1lI 									=									IIllIlI1 









                                                                                                    else                     :                    








                                                                                                                        IIIll1lI                  =                 IlI1lllI 


                                                                                                    if IIIll1lI 								==								llIlIIIl                              :                             







                                                                                                                        if not lIllllll 													:													








                                                                                                                                            IIIll1lI                              =                             l1I11II1 









                                                                                                                        else                          :                         


                                                                                                                                            IIIll1lI 														=														IlIll1l1 



                                                                                                    if IIIll1lI                        ==                       llI1lIII 												:												








                                                                                                                        IllllI1I 											=											l111lII1 

                                                                                                    if IIIll1lI                      ==                     I1IIlIIl 									:									





                                                                                                                        IllllI1I 									=									I1l1III1 









                                                                                                    if IllllI1I                 ==                l111lII1 										:										






                                                                                                                        l1llIlI1 														=														l1II1II1 
                                                                                                                        if not Il11lIll                         .                        llIl11II 												(												I11IIIll 								)								                                :                                









                                                                                                                                            l1llIlI1                 =                I111II1I 







                                                                                                                        else                            :                           






                                                                                                                                            l1llIlI1 										=										llIlIIll 









                                                                                                                        if l1llIlI1 									==									II11IllI                       :                      






                                                                                                                                            if not l1llllI1 									:									






                                                                                                                                                                l1llIlI1 								=								llIIIll1 









                                                                                                                                            else                               :                              









                                                                                                                                                                l1llIlI1 										=										ll11I1Il 


                                                                                                                        if l1llIlI1                    ==                   IIl11I1I                             :                            





                                                                                                                                            IllllI1I 										=										IlI1lllI 






                                                                                                                        if l1llIlI1                         ==                        lIlIlIll                       :                      
                                                                                                                                            IllllI1I                             =                            l1II1llI 





                                                                                                    if IllllI1I 															==															I1IIlIIl                         :                        


                                                                                                                        IlIIl11l                    =                   llI111ll 





                                                                                                    if IllllI1I 													==													l1II1llI                   :                  





                                                                                                                        IlIIl11l                   =                  IIlIIl1l 


                                                                                if IlIIl11l 									==									I1l1llII                               :                              








                                                                                                    lIIll1ll                                =                               l11111II 

                                                                                if IlIIl11l 								==								IIlIl1I1 													:													




                                                                                                    lIIll1ll 													=													l111I11l 




                                                            if lIIll1ll                                ==                               IIII1IlI                      :                     





                                                                                llIllIII                          =                         I11lIIII 





                                                            if lIIll1ll                                 ==                                IIIll1Il                         :                        



                                                                                llIllIII 										=										l111l1II 









                                                            if llIllIII                    ==                   IIlllll1 															:															




                                                                                lI11I1ll                                 =                                llll11II 









                                                                                if not Il11lIll                             .                            llIl11II                                 (                                II1llllI                 )                																:																




                                                                                                    lI11I1ll 											=											IIllIlI1 
                                                                                else                        :                       







                                                                                                    lI11I1ll                   =                  lll1l1ll 









                                                                                if lI11I1ll                       ==                      IIllIlI1                                 :                                




                                                                                                    if not IIII11lI                        (                       II11IllI                         ,                        IIllIIIl 													)																													:																








                                                                                                                        lI11I1ll                   =                  lll1Il1I 









                                                                                                    else 																:																







                                                                                                                        lI11I1ll 																=																Il1IllIl 





                                                                                if lI11I1ll                                ==                               lll1l1ll                       :                      





                                                                                                    llIllIII                   =                  l11l1lII 








                                                                                if lI11I1ll                       ==                      llI111ll                          :                         

                                                                                                    llIllIII 								=								l1IllI1l 
                                                            if llIllIII 									==									l11l1lII 																:																

                                                                                for lll11III in lllI1II1 															:															


                                                                                                    I1Il1llI 										=										IlI1lllI 




                                                                                                    Ill1lllI 										=										I111lIII 


                                                                                                    I1llIlI1 															=															IIl1I1Il 



                                                                                                    lllllI11 											=											l1llIll1 







                                                                                                    l1l1IllI                  =                 I1l1I11I 





                                                                                                    if not ll1I11II 																(																I111lI1I 														,														I1llll1l                             )                            												:												




                                                                                                                        l1l1IllI 										=										lIllll11 






                                                                                                    else                           :                          



                                                                                                                        l1l1IllI 													=													I1l1I111 





                                                                                                    if l1l1IllI                       ==                      lIllll11                     :                    








                                                                                                                        if not I1llll11                         (                        l1ll1llI 									)									                             :                             

                                                                                                                                            l1l1IllI 																=																IlIlIll1 
                                                                                                                        else                             :                            


                                                                                                                                            l1l1IllI                      =                     Il1IllIl 


                                                                                                    if l1l1IllI 												==												I1l1I111                   :                  



                                                                                                                        lllllI11 												=												I11I11lI 









                                                                                                    if l1l1IllI                       ==                      llI111ll                      :                     






                                                                                                                        lllllI11                                 =                                l1l1lIl1 








                                                                                                    if lllllI11 																==																llIIlI1I 												:												





                                                                                                                        I1lIlIl1 											=											ll1III1I 


                                                                                                                        if not l1111l1l                         (                        I1l1lIll                           )                          												:												






                                                                                                                                            I1lIlIl1                            =                           llIII1lI 




                                                                                                                        else                 :                









                                                                                                                                            I1lIlIl1                  =                 II11Illl 








                                                                                                                        if I1lIlIl1                   ==                  l111I11l 								:								






                                                                                                                                            if not II1l1Il1 										:										

                                                                                                                                                                I1lIlIl1 										=										IIl1l11I 


                                                                                                                                            else                              :                             



                                                                                                                                                                I1lIlIl1 											=											IlI1lllI 






                                                                                                                        if I1lIlIl1 												==												I1IIlIIl                         :                        






                                                                                                                                            lllllI11 																=																II11IlIl 

                                                                                                                        if I1lIlIl1                              ==                             lllIII1l                                 :                                




                                                                                                                                            lllllI11                                 =                                II11Illl 








                                                                                                    if lllllI11                  ==                 lIIl1lI1 															:															





                                                                                                                        I1llIlI1 															=															I11lIIII 





                                                                                                    if lllllI11                      ==                     II11IlIl 											:											









                                                                                                                        I1llIlI1                           =                          IIlIl11l 




                                                                                                    if I1llIlI1                    ==                   I111II1I                      :                     





                                                                                                                        IIIlI11l 											=											lII11l1I 





                                                                                                                        I11I1l1l                       =                      Ill1I11l 





                                                                                                                        if not Il11lIll 											.											llIl11II                    (                   lI1llI11                               )                              													:													







                                                                                                                                            I11I1l1l                         =                        I1I11IIl 





                                                                                                                        else                          :                         







                                                                                                                                            I11I1l1l                        =                       l1llIIll 




                                                                                                                        if I11I1l1l                        ==                       l1I1I1Il                          :                         
                                                                                                                                            if not I1llll11                          (                         ll1111l1 								)																	:									







                                                                                                                                                                I11I1l1l                            =                           l1llIIll 




                                                                                                                                            else 												:												



                                                                                                                                                                I11I1l1l 									=									lll11111 
                                                                                                                        if I11I1l1l 															==															l1II1llI                              :                             


                                                                                                                                            IIIlI11l                            =                           l1ll1Il1 



                                                                                                                        if I11I1l1l                      ==                     lll11111                         :                        

                                                                                                                                            IIIlI11l 												=												IIlI1I11 




                                                                                                                        if IIIlI11l                       ==                      I1l1IIIl 											:											




                                                                                                                                            l11IIlII                              =                             II1IIIll 



                                                                                                                                            if not IlIIII1l                              (                             Illl11II                           ,                          Il11111l                      )                     								:								
                                                                                                                                                                l11IIlII 															=															Illl11II 








                                                                                                                                            else 											:											






                                                                                                                                                                l11IIlII 											=											II11111I 







                                                                                                                                            if l11IIlII 								==								III1ll1I 															:															






                                                                                                                                                                if not llI1IlIl                            :                           
                                                                                                                                                                                    l11IIlII 								=								IIl1Il1l 




                                                                                                                                                                else 														:														







                                                                                                                                                                                    l11IIlII 																=																Il111IIl 






                                                                                                                                            if l11IIlII                       ==                      I1I11IIl 										:										



                                                                                                                                                                IIIlI11l                  =                 IllIIII1 









                                                                                                                                            if l11IIlII 									==									lIllllll 													:													









                                                                                                                                                                IIIlI11l                 =                lll11111 




                                                                                                                        if IIIlI11l 													==													IIlI1I11                             :                            



                                                                                                                                            I1llIlI1 																=																IIlIIl1l 





                                                                                                                        if IIIlI11l                    ==                   IlI1ll1l 															:															



                                                                                                                                            I1llIlI1 														=														lIlI1II1 




                                                                                                    if I1llIlI1                  ==                 lll11111 													:													








                                                                                                                        Ill1lllI                                =                               II1I11ll 






                                                                                                    if I1llIlI1                         ==                        I1l1llII                        :                       
                                                                                                                        Ill1lllI 													=													l1I11IlI 

                                                                                                    if Ill1lllI                               ==                              I11Il111                  :                 









                                                                                                                        if not llllIIII                                 (                                lIl1I1ll                          ,                         IIIl1l1l 											)											                  :                  





                                                                                                                                            Ill1lllI 														=														IlIIl1ll 



                                                                                                                        else 											:											









                                                                                                                                            Ill1lllI 										=										I1l1II1l 
                                                                                                    if Ill1lllI                          ==                         l1I11IlI 											:											






                                                                                                                        I1Il1llI 											=											Il111ll1 



                                                                                                    if Ill1lllI                      ==                     lll1Il1I                         :                        








                                                                                                                        I1Il1llI 											=											I1llll1l 








                                                                                                    if I1Il1llI 											==											lll11IIl 								:								







                                                                                                                        ll1I1lIl 												=												I111l111 








                                                                                                                        if not Il11lIll 								.								llIl11II                    (                   l1llIIll 															)																									:										




                                                                                                                                            ll1I1lIl                              =                             IllIlI1l 

                                                                                                                        else 									:									









                                                                                                                                            ll1I1lIl                             =                            lI1IlI11 






                                                                                                                        if ll1I1lIl 														==														IllIlI1l                  :                 


                                                                                                                                            if not IIl1Il1l                                :                               



                                                                                                                                                                ll1I1lIl                              =                             lI1IlI11 






                                                                                                                                            else                              :                             



                                                                                                                                                                ll1I1lIl                                 =                                l1ll1Il1 


                                                                                                                        if ll1I1lIl                          ==                         I1l1II1l 															:															





                                                                                                                                            I1Il1llI 														=														llI1II11 









                                                                                                                        if ll1I1lIl 															==															lll1I1II                          :                         


                                                                                                                                            I1Il1llI                 =                I1l11lll 






                                                                                                    if I1Il1llI                          ==                         I1l11lll 															:															

                                                                                                                        lll11III 															:															Block 






                                                                                                                        lll11III 																.																force_destroy                 (                lll11III                     )                    









                                                                                                    if I1Il1llI 															==															lll1l1ll 																:																

                                                                                                                        pass 









                                                            if llIllIII                                 ==                                l111l1II                                 :                                



                                                                                pass 



                                        player 												.												right_hand                         .                        enabled 								=								fuck_up                   (                  llllIlIl 										)										







                                        player 											.											left_hand                               .                              enabled 								=								fuck_up                      (                     I11I111I                 )                

                                        player                        .                       health_bar                         .                        bar                   .                  enabled 													=													fuck_up 														(														III1IIl1                             )                            







                                        player                       .                      enabled                   =                  fuck_up 										(										II1Ill11 										)										
                                        llI1llI1                             .                            enabled 														=														fuck_up 										(										I1IlIIlI 																)																




                                        ra                                .                               enabled 								=								fuck_up                        (                       I1IlIIlI                          )                         
                                        mra                       .                      enabled                        =                       fuck_up                                 (                                II1Ill11                                )                               
                                        escmenu                                .                               enabled 										=										fuck_up                          (                         I1IlIIlI                    )                   


                                        killmenu                          .                         enabled 										=										fuck_up                    (                   llllIlIl 																)																






                                        destroy 										(										player                    .                   right_hand 														)														





                                        destroy                     (                    player                  .                 left_hand 											)											


                                        destroy                                (                               player 										.										health_bar                   .                  bar                                )                               

                                        destroy 												(												player 																)																








                                        destroy 															(															llI1llI1 													)													






                                        destroy                               (                              ra 															)															
                                        destroy 															(															mra                                )                               









                                        destroy                         (                        escmenu                               )                              

                                        destroy 												(												killmenu                 )                

                                        lIIIIll1                       .                      menu_manager                           .                          go_back                                (                                                )                 




                    global respawn 

                    def respawn 										(										                             )                             										:										


                                        global isplayerkilled 








                                        player                       .                      enabled                           =                          fuck_up 														(														l1llIIl1                                 )                                









                                        player                         .                        health 									=									fuck_up_i                              (                             l111I1I1 										)										







                                        isplayerkilled 														=														fuck_up 												(												llllIlIl 													)													


                                        player 									.									position                        =                       lIlI1Ill 







                                        player                      .                     rotation 																=																Vec3                       (                      fuck_up_i                        (                       ll1l11II 														)																							,									fuck_up_i                              (                             ll1l11II 													)																									,												fuck_up_i 								(								ll1l11II                             )                            												)												









                                        killmenu                         .                        hideMenu 								(								                               )                               




                    class KillMenu 													(													Entity 															)															                 :                 







                                        def __init__ 									(									self                          )                         															:															



                                                            I11IlIII                             =                            self 
                                                            super 													(													                       )                                                       .                                __init__                      (                     enabled 								=								fuck_up                        (                       l1llIIl1 												)												                        ,                        color 																=																color 															.															hsv                           (                          fuck_up_i 									(									Ill1II1l 									)									                                ,                                fuck_up_i 								(								lll1llIl                           )                                                     ,                           fuck_up_i                             (                            IlI11ll1                      )                     											,											fuck_up_i 									(									lIlIlll1 										)																		)								                             ,                             scale                              =                             																(																window                           .                          aspect_ratio 											,											l11111ll 												)																										,														position                       =                      													(													II11lI1I 														,														Ill1II1l 														)																														,																parent                 =                camera                       .                      ui                      ,                     model                                =                               lI1lIlIl 											)											








                                                            Text                  (                 IIII11II 													,													position                       =                      										(										Ill1II1l                        ,                       I111111l 														)																														,																scale 											=											                           (                           Il1l1IIl 										/										window                     .                    aspect_ratio                  ,                 lI11llll 												)												                     ,                     origin 										=																				(										ll1l11II 																,																II11lI1I                         )                        														,														parent                   =                  I11IlIII                        )                       






                                                            PyneButton                  (                 text 														=														l1IlIlI1                              ,                             xPos                               =                              IlI1111l 								,								yPos                            =                           lI11I11I 								,								ySize                            =                           IlIllI1l 												,												xSize 								=								II1lI11I 												/												window 										.										aspect_ratio 														,														onClick 								=								respawn                                ,                               tooltip                       =                      II111Il1                         ,                        parent 								=								I11IlIII 											)											
                                                            PyneButton 													(													text 															=															IIl1II11 								,								xPos                     =                    l1l1I1ll 												,												yPos 								=								                             -                             I11l111l 									,									ySize                        =                       IlIllI1l                              ,                             xSize 									=									IIIIllll 												/												window 																.																aspect_ratio 													,													onClick                               =                              PyneQuit                        ,                       tooltip                          =                         lIl1lIll 														,														parent 								=								I11IlIII 													)													







                                                            I11IlIII                                .                               hideMenu 														(																										)												






                                        def showMenu                              (                             self 									)																				:											





                                                            I11IIlII 												=												self 



                                                            I11IIlII 								.								visible 												=												fuck_up                        (                       II1III11 														)														








                                                            for lII1II1l in I11IIlII 															.															children                           :                          






                                                                                I11llIII                                =                               ll11Ill1 

                                                                                I1IIll1I                     =                    Ill1I11l 








                                                                                if not l1111l1l                          (                         lII11l1I 														)														                 :                 



                                                                                                    I1IIll1I 											=											I1l1I1lI 








                                                                                else 								:								









                                                                                                    I1IIll1I                  =                 Illl11II 




                                                                                if I1IIll1I 										==										IIl1Il1l                       :                      








                                                                                                    if not IlIIII1l                                 (                                I1l11lll 														,														l1l1llI1 								)								                     :                     








                                                                                                                        I1IIll1I                               =                              ll11Ill1 
                                                                                                    else 								:								









                                                                                                                        I1IIll1I 																=																llI1IlIl 





                                                                                if I1IIll1I                      ==                     ll11Ill1 										:										

                                                                                                    I11llIII                            =                           Il1llII1 

                                                                                if I1IIll1I 										==										llllI1l1                              :                             





                                                                                                    I11llIII 													=													ll1II1ll 




                                                                                if I11llIII 														==														Ill11llI                               :                              


                                                                                                    IIlII11l 														=														llI1Il1l 



                                                                                                    if not Il11lIll 														.														llIl11II                     (                    IlllIl11 																)																                            :                            







                                                                                                                        IIlII11l 														=														I1IlIIll 






                                                                                                    else 													:													


                                                                                                                        IIlII11l                               =                              llll11II 

                                                                                                    if IIlII11l 														==														lIII1lIl 										:										



                                                                                                                        II11lIII 								=								l1IllI1l 






                                                                                                                        lIlIl1I1 															=															lII11l1I 








                                                                                                                        lI1I1IIl 											=											I1IllllI 



                                                                                                                        if not IIII11lI                                 (                                lll1111l 																,																lll1111l 								)								                 :                 
                                                                                                                                            lI1I1IIl                            =                           llII1llI 









                                                                                                                        else 															:															









                                                                                                                                            lI1I1IIl                    =                   IllIlI1l 







                                                                                                                        if lI1I1IIl                 ==                IIII1IlI 										:										








                                                                                                                                            if not I111l111                 :                

                                                                                                                                                                lI1I1IIl                           =                          Il1l11I1 




                                                                                                                                            else                     :                    









                                                                                                                                                                lI1I1IIl 														=														III1ll1I 







                                                                                                                        if lI1I1IIl 								==								Ill111l1 																:																



                                                                                                                                            lIlIl1I1                  =                 IIl11II1 




                                                                                                                        if lI1I1IIl 									==									III1ll1I                                 :                                

                                                                                                                                            lIlIl1I1 																=																l1I11II1 



                                                                                                                        if lIlIl1I1                    ==                   l1l1l11I                                 :                                









                                                                                                                                            II111ll1                    =                   I11I11lI 






                                                                                                                                            if not I1llll11                               (                              IllIIII1                                )                                                        :                         







                                                                                                                                                                II111ll1                                 =                                IllIl11I 







                                                                                                                                            else 											:											


                                                                                                                                                                II111ll1                                =                               IIl11II1 









                                                                                                                                            if II111ll1 																==																ll1III1I 											:											







                                                                                                                                                                if not l1111l1l 								(								ll11IlII                              )                                                :                   






                                                                                                                                                                                    II111ll1 											=											IIll11I1 




                                                                                                                                                                else                              :                             



                                                                                                                                                                                    II111ll1                 =                lIlIlIll 





                                                                                                                                            if II111ll1 																==																Il1llII1                    :                   



                                                                                                                                                                lIlIl1I1                              =                             Ill1IIIl 






                                                                                                                                            if II111ll1                    ==                   l1l1IIIl 												:												


                                                                                                                                                                lIlIl1I1 													=													I1IlII11 



                                                                                                                        if lIlIl1I1 															==															ll1III1I 								:								






                                                                                                                                            II11lIII 											=											llI1Il1l 






                                                                                                                        if lIlIl1I1 															==															III1ll1I                           :                          







                                                                                                                                            II11lIII 										=										llIIIll1 

                                                                                                                        if II11lIII                            ==                           II1IIIll                  :                 







                                                                                                                                            II1Il11I                              =                             l1IIllI1 







                                                                                                                                            Il111lI1 										=										II1III1I 






                                                                                                                                            if not llllIIII 									(									l1111Ill                   ,                  I1IllllI                          )                         									:									





                                                                                                                                                                Il111lI1                         =                        I111l111 









                                                                                                                                            else                         :                        
                                                                                                                                                                Il111lI1 											=											IlllIIl1 





                                                                                                                                            if Il111lI1                      ==                     IlllI1lI 										:										

                                                                                                                                                                if not l1111l1l                  (                 IlIllll1                         )                                                   :                           





                                                                                                                                                                                    Il111lI1 															=															I111l1II 









                                                                                                                                                                else 														:														







                                                                                                                                                                                    Il111lI1 															=															l11IlI1I 



                                                                                                                                            if Il111lI1                            ==                           I111l1II 									:									






                                                                                                                                                                II1Il11I                             =                            IIlIl1I1 

                                                                                                                                            if Il111lI1                    ==                   I111l111                                :                               




                                                                                                                                                                II1Il11I 															=															ll1Il1II 




                                                                                                                                            if II1Il11I                          ==                         Il1IllIl                            :                           

                                                                                                                                                                llI11III 																=																llllI1l1 







                                                                                                                                                                if not l1111l1l                 (                IllIlII1                           )                                                :                      








                                                                                                                                                                                    llI11III                     =                    IIIlIIlI 





                                                                                                                                                                else                       :                      




                                                                                                                                                                                    llI11III                    =                   IllIlII1 




                                                                                                                                                                if llI11III 									==									llIIlI1I                     :                    
                                                                                                                                                                                    if not l1111l1l 													(													l1lI1I1I                 )                										:										

                                                                                                                                                                                                        llI11III 									=									lllI1ll1 








                                                                                                                                                                                    else 											:											





                                                                                                                                                                                                        llI11III 										=										I1IIlIIl 




                                                                                                                                                                if llI11III                       ==                      l1I11II1                           :                          
                                                                                                                                                                                    II1Il11I                           =                          ll1111lI 







                                                                                                                                                                if llI11III 														==														IllIlII1                           :                          



                                                                                                                                                                                    II1Il11I                                =                               lllIIlll 




                                                                                                                                            if II1Il11I                          ==                         ll11I1Il 														:														
                                                                                                                                                                II11lIII 															=															l1I11IlI 







                                                                                                                                            if II1Il11I                     ==                    l1lI1lI1 												:												









                                                                                                                                                                II11lIII 												=												lIlIlIll 

                                                                                                                        if II11lIII                                ==                               llIIIll1                                :                               
                                                                                                                                            IIlII11l 									=									Il1l1IlI 








                                                                                                                        if II11lIII                  ==                 l1I11IlI                                :                               






                                                                                                                                            IIlII11l                        =                       lIlI11I1 
                                                                                                    if IIlII11l                 ==                I1IlIIll                  :                 




                                                                                                                        I11llIII 											=											I1l1lIll 



                                                                                                    if IIlII11l                                ==                               lllI1l1l 																:																


                                                                                                                        I11llIII                          =                         IllIl11I 



                                                                                if I11llIII                    ==                   l11l1lII                     :                    






                                                                                                    pass 

                                                                                if I11llIII 														==														Il1llII1 												:												



                                                                                                    ll1IllIl 									=									l1llIIIl 





                                                                                                    lllI11l1 													=													IIl1Il1l 









                                                                                                    if lI11I1l1 										(										IIl11lll                     ,                    llIlIII1 										)																										:																



                                                                                                                        lllI11l1                  =                 ll1111lI 




                                                                                                    else                              :                             
                                                                                                                        lllI11l1                             =                            I11I11lI 
                                                                                                    if lllI11l1 									==									ll1111lI 															:															




                                                                                                                        if not l1111l1l                     (                    l1llIIll                              )                             													:													






                                                                                                                                            lllI11l1 															=															I1llI11I 







                                                                                                                        else 															:															







                                                                                                                                            lllI11l1                          =                         I11I11lI 

                                                                                                    if lllI11l1                      ==                     IIIlIIlI                       :                      








                                                                                                                        ll1IllIl 																=																IIl1l11I 





                                                                                                    if lllI11l1                            ==                           Il1lIlI1 													:													







                                                                                                                        ll1IllIl 											=											llI1lIII 

                                                                                                    if ll1IllIl 										==										II11Illl                        :                       



                                                                                                                        IlIl1l1I                 =                l1I1lII1 

                                                                                                                        if IlIIII1l 											(											lI1llI11 													,													Ill11llI                 )                                                :                                


                                                                                                                                            IlIl1l1I 											=											IlIIl1ll 







                                                                                                                        else                   :                  
                                                                                                                                            IlIl1l1I                              =                             ll1II1ll 


                                                                                                                        if IlIl1l1I 																==																ll1lll1l                        :                       





                                                                                                                                            if not IlIlI1II                     (                    lII1II1l 													,													Entity                       )                                          :                    




                                                                                                                                                                IlIl1l1I 									=									ll11I1Il 






                                                                                                                                            else 											:											


                                                                                                                                                                IlIl1l1I                      =                     ll11III1 









                                                                                                                        if IlIl1l1I                               ==                              ll1Il1II                           :                          




                                                                                                                                            ll1IllIl 											=											II1I11ll 







                                                                                                                        if IlIl1l1I 														==														llI1II11                       :                      






                                                                                                                                            ll1IllIl 														=														IlIll1l1 









                                                                                                    if ll1IllIl 										==										l1IIl1ll                                 :                                









                                                                                                                        pass 








                                                                                                    if ll1IllIl 										==										llI1lIII 												:												







                                                                                                                        pass 








                                                                                                    lII1II1l 									.									enabled 								=								fuck_up 										(										lllI1111                        )                       



                                                            IIllIllI                         .                        play 													(																								)											










                                        def hideMenu 																(																self 										)										                :                
                                                            Il11lIIl 													=													self 



                                                            Il11lIIl 											.											visible                           =                          fuck_up                                (                               lIIIIIII                 )                








                                                            for I1lIl1II in Il11lIIl                           .                          children 																:																








                                                                                IlI1Ill1                   =                  I1I1l11l 








                                                                                IllIIll1 															=															llll11II 



                                                                                if not l1111l1l 										(										IllIlII1                         )                        											:											







                                                                                                    IllIIll1                          =                         II111lIl 


                                                                                else                              :                             






                                                                                                    IllIIll1                   =                  l1llIIll 







                                                                                if IllIIll1 														==														I111lIII 													:													

                                                                                                    IlIIl11I                  =                 lIlIlIll 


                                                                                                    lII11111                              =                             IIl1Il1l 









                                                                                                    IlI1llI1                                =                               llI1Il1l 


                                                                                                    if not l1lll1II 													:													

                                                                                                                        IlI1llI1                               =                              l1lll1II 

                                                                                                    else                                 :                                








                                                                                                                        IlI1llI1                          =                         ll11I1Il 




                                                                                                    if IlI1llI1                       ==                      ll11I1Il 																:																







                                                                                                                        if not I1llll11 												(												IIlIIl1l                               )                              										:										









                                                                                                                                            IlI1llI1                             =                            I1l1lIll 


                                                                                                                        else                  :                 
                                                                                                                                            IlI1llI1 										=										III1111l 

                                                                                                    if IlI1llI1                     ==                    III1111l                   :                  


                                                                                                                        lII11111                           =                          ll1III1I 



                                                                                                    if IlI1llI1                             ==                            l1lll1II 								:								






                                                                                                                        lII11111 												=												I1l1I111 





                                                                                                    if lII11111                               ==                              ll1III1I 													:													









                                                                                                                        II1I1I11                            =                           I1l1IIIl 





                                                                                                                        if not Il11lIll 												.												llIl11II                  (                 llI1II11                              )                                               :                  







                                                                                                                                            II1I1I11                           =                          l111I11l 




                                                                                                                        else 									:									


                                                                                                                                            II1I1I11 										=										Il1I111I 

                                                                                                                        if II1I1I11 										==										l11Il1l1 									:									








                                                                                                                                            if not lIl1I11I                             (                            llIIIll1                               ,                              IllIl11I 										)																						:												




                                                                                                                                                                II1I1I11                  =                 Il1I1lll 



                                                                                                                                            else 														:														







                                                                                                                                                                II1I1I11                           =                          l1lIlI1l 








                                                                                                                        if II1I1I11                        ==                       II111I1I                    :                   






                                                                                                                                            lII11111                                 =                                IlIlIll1 









                                                                                                                        if II1I1I11                   ==                  Il1I1lll                     :                    


                                                                                                                                            lII11111 												=												I1IIlIIl 







                                                                                                    if lII11111 									==									IlI1lllI                                :                               


                                                                                                                        IlIIl11I                 =                IIlIlIlI 



                                                                                                    if lII11111 										==										l11lIlII                  :                 




                                                                                                                        IlIIl11I                         =                        l11l1lII 








                                                                                                    if IlIIl11I 								==								I1l1lIll                                 :                                




                                                                                                                        lII11IIl 										=										llI1II11 



                                                                                                                        IlII1lIl                                 =                                I1l1I111 






                                                                                                                        if not l1111l1l 																(																lIII1III 													)													                         :                         






                                                                                                                                            IlII1lIl 											=											I11IIIll 
                                                                                                                        else                              :                             









                                                                                                                                            IlII1lIl                            =                           I1lllIl1 





                                                                                                                        if IlII1lIl 												==												I1lllIl1 															:															







                                                                                                                                            if not ll1I11II                                (                               Il11l111 																,																l1llll1I 													)													                  :                  



                                                                                                                                                                IlII1lIl 										=										II1lIIll 









                                                                                                                                            else 								:								


                                                                                                                                                                IlII1lIl                      =                     I11IIIll 



                                                                                                                        if IlII1lIl                           ==                          II11IIlI 												:												







                                                                                                                                            lII11IIl 												=												IlI1lllI 


                                                                                                                        if IlII1lIl 									==									II1lIIll                              :                             


                                                                                                                                            lII11IIl 											=											ll1II1ll 
                                                                                                                        if lII11IIl                               ==                              II1III1I                  :                 


                                                                                                                                            IlIIIIIl                            =                           Ill1I11l 







                                                                                                                                            if not Il11lIll                  .                 llIl11II                               (                              Il11llll 								)								                        :                        
                                                                                                                                                                IlIIIIIl                            =                           I1IlIIII 




                                                                                                                                            else 															:															







                                                                                                                                                                IlIIIIIl                      =                     l1llIIIl 



                                                                                                                                            if IlIIIIIl                              ==                             l11111II 											:											









                                                                                                                                                                if not l1l1Il1l                         :                        



                                                                                                                                                                                    IlIIIIIl 														=														ll1l1I11 









                                                                                                                                                                else                      :                     



                                                                                                                                                                                    IlIIIIIl                                 =                                I1IlIIII 


                                                                                                                                            if IlIIIIIl                  ==                 lI1l11lI 											:											





                                                                                                                                                                lII11IIl                       =                      lll11IIl 





                                                                                                                                            if IlIIIIIl                                 ==                                ll1l1I11 								:								




                                                                                                                                                                lII11IIl                  =                 IIlI111I 



                                                                                                                        if lII11IIl 															==															l1l1ll1I 												:												





                                                                                                                                            IlIIl11I                   =                  IIIlI1lI 






                                                                                                                        if lII11IIl 								==								IlI1IIII 									:									





                                                                                                                                            IlIIl11I 											=											l11111II 



                                                                                                    if IlIIl11I                   ==                  l1ll1III                     :                    

                                                                                                                        IllIIll1 												=												Ill111l1 


                                                                                                    if IlIIl11I                       ==                      llII1llI 										:										


                                                                                                                        IllIIll1 											=											l11I1IlI 
                                                                                if IllIIll1 								==								Ill111l1                    :                   




                                                                                                    IlI1Ill1                               =                              I11Il111 

                                                                                if IllIIll1 														==														IIll1IlI                   :                  
                                                                                                    IlI1Ill1                  =                 IlIIIlIl 
                                                                                if IlI1Ill1                     ==                    ll1lIIIl 													:													







                                                                                                    ll1lIllI 									=									l1l1Il1l 








                                                                                                    if not Il11lIll                                 .                                llIl11II 															(															l1IIllI1 								)																						:														




                                                                                                                        ll1lIllI 																=																ll1I1ll1 






                                                                                                    else                     :                    

                                                                                                                        ll1lIllI 												=												I111lIII 
                                                                                                    if ll1lIllI 										==										l1IIl1ll                         :                        



                                                                                                                        if not l1111l1l 												(												Il1lIl1l 														)																												:														


                                                                                                                                            ll1lIllI                   =                  l1llIIll 





                                                                                                                        else 																:																



                                                                                                                                            ll1lIllI                            =                           lIII1lIl 






                                                                                                    if ll1lIllI                        ==                       IIl111I1 											:											



                                                                                                                        IlI1Ill1                      =                     I11Il111 


                                                                                                    if ll1lIllI 											==											l11111Il 													:													





                                                                                                                        IlI1Ill1 															=															Il1lIlI1 
                                                                                if IlI1Ill1                           ==                          I11Il111                                 :                                




                                                                                                    pass 


                                                                                if IlI1Ill1                            ==                           I1llI11I                      :                     









                                                                                                    I1I1llII                         =                        I1I11IIl 





                                                                                                    IIlIlllI 														=														llI1IlIl 




                                                                                                    if IIII11lI                        (                       lll11111                        ,                       lIlI1II1                            )                           														:														








                                                                                                                        IIlIlllI                  =                 llIllIlI 
                                                                                                    else                  :                 

                                                                                                                        IIlIlllI                       =                      IIII1IlI 
                                                                                                    if IIlIlllI 												==												l11111II 										:										



                                                                                                                        if llllIIII 								(								Il1llIIl                             ,                            II1l11Il 									)																								:															


                                                                                                                                            IIlIlllI                          =                         ll1111lI 








                                                                                                                        else 															:															


                                                                                                                                            IIlIlllI 														=														II11IllI 


                                                                                                    if IIlIlllI                          ==                         IIlIl11l                          :                         





                                                                                                                        I1I1llII                               =                              ll1III1I 






                                                                                                    if IIlIlllI 														==														IlI1I1I1                  :                 

                                                                                                                        I1I1llII                        =                       II1I11ll 







                                                                                                    if I1I1llII 															==															I11Il111                           :                          








                                                                                                                        lIll1lII 								=								I11Il111 








                                                                                                                        if not I1I1lIlI 														(														I1lIl1II                          ,                         Entity                           )                          																:																
                                                                                                                                            lIll1lII                  =                 llIlIIll 






                                                                                                                        else                         :                        








                                                                                                                                            lIll1lII                       =                      lll1l1ll 


                                                                                                                        if lIll1lII                         ==                        llIlIIll                       :                      




                                                                                                                                            if not l1111l1l                   (                  II11lI1I                 )                										:										









                                                                                                                                                                lIll1lII                          =                         l1111Ill 








                                                                                                                                            else                             :                            
                                                                                                                                                                lIll1lII                           =                          I1IIlIIl 



                                                                                                                        if lIll1lII                     ==                    lll1l1ll                         :                        









                                                                                                                                            I1I1llII                             =                            II11111I 






                                                                                                                        if lIll1lII 															==															l1l1l11I 											:											

                                                                                                                                            I1I1llII                       =                      I11ll1I1 
                                                                                                    if I1I1llII                       ==                      II11111I 																:																



                                                                                                                        pass 

                                                                                                    if I1I1llII                            ==                           I1lllIl1 														:														




                                                                                                                        pass 
                                                                                                    I1lIl1II                      .                     enabled                 =                fuck_up 																(																lIIIIIII                          )                         

                    global killmenu 

                    killmenu 											=											KillMenu                       (                                                      )                                


                    global kill 



                    def kill                               (                                                              )                                                 :                 




                                        global isplayerkilled 






                                        isplayerkilled 								=								fuck_up                   (                  l1llIIl1                            )                           



                                        Il11I11I                      =                     lIlI1ll1 




                                        llll1I1I 								=								IIIlIIlI 








                                        if not Il11lIll                 .                llIl11II 										(										lIllll11                             )                            															:															




                                                            llll1I1I                  =                 IIl1I1Il 






                                        else 										:										


                                                            llll1I1I 														=														lllI1l1l 
                                        if llll1I1I 														==														lIlI11I1 										:										
                                                            if not ll1I11II                                (                               IIlIl11l 												,												Illl1I11                      )                                       :                  






                                                                                llll1I1I 											=											IIl11lll 
                                                            else 													:													





                                                                                llll1I1I 													=													I1llll1l 



                                        if llll1I1I 								==								lIllIIll 									:									





                                                            Il11I11I 								=								llIlIIIl 







                                        if llll1I1I 													==													I1lI1lIl 												:												






                                                            Il11I11I                     =                    llI11llI 


                                        if Il11I11I                     ==                    llI11llI 									:									




                                                            lI1I1lI1                  =                 Il11I111 







                                                            if not IIII11lI 														(														isplayerkilled                   ,                  fuck_up                     (                    l1IIlII1                               )                              								)								                          :                          







                                                                                lI1I1lI1 													=													l1l1l11I 





                                                            else                        :                       







                                                                                lI1I1lI1                     =                    I1lIl1ll 




                                                            if lI1I1lI1 														==														I1lIl1ll                       :                      






                                                                                if not III1111l 									:									








                                                                                                    lI1I1lI1 													=													l1l1l11I 

                                                                                else                          :                         









                                                                                                    lI1I1lI1 													=													llI1Il1l 







                                                            if lI1I1lI1                    ==                   II1III1I 																:																




                                                                                Il11I11I                               =                              IIllIlI1 









                                                            if lI1I1lI1                              ==                             l11l1I11 																:																





                                                                                Il11I11I 											=											I11ll1I1 

                                        if Il11I11I 									==									IIl11II1                        :                       





                                                            pass 



                                        if Il11I11I                 ==                llIlIIIl 											:											




                                                            player                                 .                                enabled 									=									fuck_up 														(														I1IlIIlI                                )                               




                                                            killmenu                      .                     showMenu 								(								                   )                   





                    global returntogame 










                    def returntogame                                (                               								)								                             :                             






                                        global escmenuenabled 

                                        player                         .                        enabled                    =                   fuck_up 									(									IlIl11Il 														)														







                                        escmenuenabled 								=								fuck_up                               (                              II1Ill11                        )                       


                                        escmenu                         .                        hideMenu                  (                 														)														


                    class RickAstley 															(															Entity 													)																										:													








                                        def __init__ 																(																self                           ,                          position                             =                            												(												ll1l11II                     ,                    lI11llll 									,									II11lI1I 														)														                             )                             													:													
                                                            (                IIlII1II                             ,                            lll1lII1                 )                                                =                                                                (                                self 									,									position                               )                              




                                                            super 										(										                           )                                                  .                       __init__ 								(								parent                              =                             scene 									,									position 											=											lll1lII1                   ,                  model                                =                               IIl1I111 										,										texture                        =                       I1I1lII1                              ,                             scale                    =                   l111l1II                                ,                               collider                            =                           lIlI1111                         )                        




                    global ra 


                    ra 																=																RickAstley                                (                               position 										=										                       (                       I11IlI1l 														,														II1l1I1I 																,																I11IlI1l 																)																															)															



                    class MiniRickAsltey 												(												Entity 													)													                 :                 

                                        def __init__ 								(								self 												,												position 														=														ra                          .                         position                              )                             																:																








                                                            (														IIII1l1l 														,														lIIII11l 									)									                                =                                												(												position 									,									self                      )                     





                                                            super 															(															                      )                      											.											__init__ 									(									parent                    =                   scene 											,											position 									=									IIII1l1l 												,												model                          =                         IIl1I111 									,									texture                                =                               I1I1lII1                                ,                               scale 												=												lIl11II1                           ,                          collider 													=													llllI11I                          )                         






                    global mra 





                    mra 												=												MiniRickAsltey 												(																											)															








                    class Cursor                       (                      Entity 											)											                           :                           


                                        def __init__ 															(															self                           )                          								:								



                                                            l111Illl                            =                           self 






                                                            super                       (                      										)																										.																__init__ 												(												parent                                =                               camera                             .                            ui 													,													position 								=																							(															l1IIII1I 								,								II11lI1I                                )                               										,										texture 											=											III1ll11                     ,                    model 															=															I1l1II11 														,														scale 											=											lI1IlI11 									/																					(												window 										.										aspect_ratio 											*											Ill1lIl1                  )                 											,											color 											=											color                    .                   white 									)									


                                                            l111Illl 											.											always_on_top_setter 									(									fuck_up                             (                            l1llIIl1 										)																								)														









                                        def update 																(																self 									)									                              :                              






                                                            l1Il1lI1                               =                              self 






                                                            IIIIIl1I 											=											lIlIl1ll 









                                                            l1I1l11I 														=														lllII1ll 




                                                            if not llllIIII                  (                 IllIlII1                 ,                llllIlI1                            )                           												:												



                                                                                l1I1l11I 								=								lIlIl1ll 









                                                            else 										:										








                                                                                l1I1l11I 											=											l11I1IlI 



                                                            if l1I1l11I                          ==                         l11Il1l1 															:															




                                                                                if not I1llll11                      (                     lIII1III                             )                            													:													

                                                                                                    l1I1l11I 									=									l11I1IlI 

                                                                                else                           :                          




                                                                                                    l1I1l11I 								=								l1lIlI1l 

                                                            if l1I1l11I 									==									IlI11llI                           :                          









                                                                                IIIIIl1I                             =                            I1l1III1 
                                                            if l1I1l11I 													==													IIl1I1Il 									:									






                                                                                IIIIIl1I 														=														lIII1III 


                                                            if IIIIIl1I                  ==                 l1l1l11I                            :                           



                                                                                l11I1lI1                           =                          lIllllll 



                                                                                if not player 																.																enabled                 :                
                                                                                                    l11I1lI1 											=											II11IlIl 






                                                                                else                  :                 





                                                                                                    l11I1lI1 														=														ll11IlIl 




                                                                                if l11I1lI1                   ==                  ll1lIIIl                  :                 


                                                                                                    if not IIII11lI 								(								Illl1II1 													,													Illl1II1 													)																							:										
                                                                                                                        l11I1lI1                   =                  II1IlII1 



                                                                                                    else                               :                              








                                                                                                                        l11I1lI1                 =                I1lIIl1I 





                                                                                if l11I1lI1                               ==                              l1ll1III                          :                         



                                                                                                    IIIIIl1I                    =                   ll11IlI1 




                                                                                if l11I1lI1                        ==                       lIllllII                           :                          







                                                                                                    IIIIIl1I 									=									I1lll11I 


                                                            if IIIIIl1I 													==													IIII11ll                              :                             






                                                                                l1Il1lI1 										.										position_setter                     (                                            (                        fuck_up_i 											(											mouse                                 .                                x                        )                       									,									fuck_up_i                                 (                                mouse                      .                     y 												)												                      )                                                   )                             

                                                                                mouse 														.														visible                       =                      fuck_up 								(								I1IlIIlI                        )                       


                                                            if IIIIIl1I 											==											Ill111l1                     :                    






                                                                                l1Il1lI1                   .                  position_setter 											(																								(													fuck_up 												(												IIIl111I 																)																									,									fuck_up                                (                               l1IIII1I                       )                                               )                         									)									


                    global cursor 

                    cursor 										=										Cursor                              (                             												)												


                    lllI1II1                                 =                                                [                															]															






                    global prev_player_position 







                    prev_player_position 														=														player 												.												position 





                    Il1lI1lI 														=														II1llIll 								/								lIllll11 







                    class Block                                 (                                Button                          )                                                      :                             









                                        is_destroyed                 :                Il1Il1I1 








                                        is_reachable 											:											Il1Il1I1 










                                        def __init__                 (                self 																,																texture                    ,                   position 													=																									(												II11lI1I                              ,                             IIIl111I 															,															II11lI1I                  )                                           )                          														:														







                                                            (                             I1ll1111 											,											I1IIlIl1                      ,                     l11l1llI 									)																						=																					(								texture 															,															self                                 ,                                position                  )                 







                                                            super 															(																										)																										.															__init__                              (                             parent                                 =                                scene                               ,                              position                            =                           l11l1llI                                ,                               model                     =                    II1llIlI 										,										origin_y 												=												ll1lI11l 								,								texture                         =                        I1ll1111 									,									color                          =                         color 									.									color                        (                       ll1l11II                            ,                           lIl11III                    ,                   random                          .                         uniform 													(													I111l1lI 												,												lIII1II1                   )                                   )                                         ,                        highlight_color 																=																color                                 .                                white                          ,                         scale 												=												lIlIlll1                     ,                    collider                                 =                                llllI11I 										)										







                                                            I1IIlIl1 								.								is_destroyed 															=															fuck_up                           (                          lIIIIIII 													)													







                                                            I1IIlIl1                           .                          is_reachable                  =                 fuck_up 																(																lllI1111 															)															








                                                            I1IIlIl1 								.								block_dict 														:														l1l1Ill1 											=																								{													l1l1IIIl 															:															GrassBlock                 ,                IIllIl11 																:																StoneBlock                      ,                     lI11llll 												:												BrickBlock 												,												l1I1I1Il 											:											DirtBlock                      ,                     IIIllI1I 									:									BedrockBlock                      ,                     IIl1l11I                   :                  GlassBlock                       ,                      l1llIll1                         :                        BasicWoodBlock 								,								I1l1I111                 :                BasicWoodBlockPlanks                      }                     








                                                            lllI1II1                            .                           append 														(														I1IIlIl1                        )                       







                                        II1Il1lI 





                                        lIIIl1lI 






                                        IIIII1l1 



                                        def update 													(													self                            )                                                           :                                






                                                            III1l1lI 												=												self 





                                                            l1lIllI1 											=											distance 											(											III1l1lI                               .                              position 										,										player                    .                   position 									)									


                                                            I1IIlI11                 =                IIl1III1 









                                                            lllll1I1 								=								IlIIIlIl 






                                                            if not l1111l1l 															(															I1l1llII 														)														                        :                        








                                                                                lllll1I1 														=														Ill1I11I 









                                                            else                     :                    








                                                                                lllll1I1 																=																I1llll1l 





                                                            if lllll1I1                        ==                       I1llll1l                                :                               
                                                                                if not l1111l1l 											(											l1llIl1I 												)												                   :                   




                                                                                                    lllll1I1 															=															lI1l11lI 








                                                                                else                       :                      







                                                                                                    lllll1I1 											=											Ill1I11I 

                                                            if lllll1I1 											==											I1111IlI 										:										




                                                                                I1IIlI11 										=										IlIIIlIl 









                                                            if lllll1I1                  ==                 I1lllIl1 														:														
                                                                                I1IIlI11                        =                       IIl11II1 
                                                            if I1IIlI11                 ==                I1IlII11                         :                        



                                                                                IIl1llII 															=															ll11Ill1 







                                                                                if not I1llll11                     (                    I1l11lll                                )                               										:										

                                                                                                    IIl1llII                       =                      Il1I111I 








                                                                                else 														:														








                                                                                                    IIl1llII                    =                   ll1111lI 








                                                                                if IIl1llII 										==										llIllIlI                               :                              

                                                                                                    if not llllIIII                              (                             l1lIllI1 												,												II1llIll 											)											                              :                              

                                                                                                                        IIl1llII 												=												l11Il1l1 

                                                                                                    else 										:										
                                                                                                                        IIl1llII 								=								llIII1lI 

                                                                                if IIl1llII                               ==                              l1lIlI1l                                 :                                


                                                                                                    I1IIlI11                      =                     l1l1IlIl 







                                                                                if IIl1llII 									==									Il1I111I 									:									









                                                                                                    I1IIlI11                  =                 I1l1I111 








                                                            if I1IIlI11                    ==                   lIl1I1ll 								:								






                                                                                llI11l11                   =                  IlI1I1I1 

                                                                                l11I111I 										=										l1l1Il1l 








                                                                                if not I1llll11                               (                              lI11llll                            )                                                     :                          





                                                                                                    l11I111I 									=									Il1l1IlI 


                                                                                else 										:										







                                                                                                    l11I111I                         =                        l11l1I11 






                                                                                if l11I111I 																==																IlIIl1I1 														:														

                                                                                                    if not lI11I1l1 								(								ll1III1I                                ,                               I1lI1lIl 													)													                         :                         







                                                                                                                        l11I111I                         =                        llI1l1II 









                                                                                                    else                  :                 



                                                                                                                        l11I111I                        =                       IlI1ll1l 

                                                                                if l11I111I 									==									Il11l111 												:												

                                                                                                    llI11l11                    =                   Il111IIl 






                                                                                if l11I111I                    ==                   lIlIl111                              :                             



                                                                                                    llI11l11 								=								II11111I 



                                                                                if llI11l11                               ==                              Ill1IIIl 																:																

                                                                                                    IIll1lI1 													=													l11lIlII 



                                                                                                    if not I1llI11I                          :                         
                                                                                                                        IIll1lI1                               =                              ll11I1Il 







                                                                                                    else                           :                          






                                                                                                                        IIll1lI1 																=																IIIlIIlI 





                                                                                                    if IIll1lI1                                ==                               IIIlIIlI 														:														
                                                                                                                        if not III1l1lI 											.											is_reachable                           :                          







                                                                                                                                            IIll1lI1                    =                   ll1Il1II 




                                                                                                                        else                             :                            





                                                                                                                                            IIll1lI1                         =                        ll1lll1l 




                                                                                                    if IIll1lI1                                ==                               IIlI111I 															:															


                                                                                                                        llI11l11 										=										l1l1l11I 


                                                                                                    if IIll1lI1                        ==                       IIl11I1I 													:													


                                                                                                                        llI11l11                                =                               I1llllIl 
                                                                                if llI11l11 															==															l1I1I1Il 												:												




                                                                                                    III1l1lI                              .                             is_reachable 																=																fuck_up 										(										l1IIlII1 													)													

                                                                                                    III1l1lI                             .                            highlight_color                     =                    color                 .                white 









                                                                                if llI11l11                      ==                     l1I11II1                              :                             








                                                                                                    pass 

                                                            if I1IIlI11 												==												l1l1IlIl                               :                              









                                                                                l11II1lI                          =                         lI11lIIl 









                                                                                lIlI1I11 								=								lI11lIIl 







                                                                                if not IIII11lI                       (                      llIlIIll 																,																lIIIl11l                 )                                   :                   




                                                                                                    lIlI1I11 													=													l1lll1II 








                                                                                else                 :                



                                                                                                    lIlI1I11 												=												IIIllI1I 







                                                                                if lIlI1I11 										==										Illl11II                             :                            








                                                                                                    if not III1l1lI 												.												is_reachable                                 :                                






                                                                                                                        lIlI1I11                             =                            Il1l11I1 








                                                                                                    else 										:										








                                                                                                                        lIlI1I11 											=											I1l1lIll 


                                                                                if lIlI1I11 											==											Ill111l1                          :                         






                                                                                                    l11II1lI 													=													III1ll1I 





                                                                                if lIlI1I11                     ==                    l1lll1II 												:												



                                                                                                    l11II1lI 										=										lIl1I1ll 




                                                                                if l11II1lI 								==								l1l111l1 												:												


                                                                                                    I1I1l1I1                 =                lIIIl11l 






                                                                                                    if not lI11I1l1                  (                 lIll1I1l 								,								lI111lIl                          )                         															:															







                                                                                                                        I1I1l1I1 										=										l11l1I11 


                                                                                                    else 										:										

                                                                                                                        I1I1l1I1                       =                      II1lllII 






                                                                                                    if I1I1l1I1                   ==                  l1llllI1                       :                      




                                                                                                                        if not l1111l1l                              (                             l1l1lIl1 														)														                                :                                






                                                                                                                                            I1I1l1I1 												=												llI1II11 



                                                                                                                        else                     :                    



                                                                                                                                            I1I1l1I1                         =                        IlIIl1I1 








                                                                                                    if I1I1l1I1                 ==                IlIIl1I1                            :                           








                                                                                                                        l11II1lI 															=															I111II1I 





                                                                                                    if I1I1l1I1                                ==                               lll1l1ll                 :                
                                                                                                                        l11II1lI 										=										III1ll1I 
                                                                                if l11II1lI                 ==                IIlIl11l 															:															





                                                                                                    III1l1lI 																.																is_reachable                   =                  fuck_up 														(														I1IlIIlI                  )                 




                                                                                                    III1l1lI 											.											highlight_color 										=										color 								.								black 





                                                                                if l11II1lI 													==													II11111I 																:																


                                                                                                    pass 








                                        def input 											(											self                  ,                 key                 )                                 :                 





                                                            (                          IlIlIIlI 									,									l1lI1Ill                             )                                                     =                                               (                      key                         ,                        self 												)												







                                                            llIll11l 													=													l1l1ll1I 

                                                            I11l1llI 											=											IlI1I1I1 




                                                            llI1l1l1 								=								I1l1III1 

                                                            if not l1lI1Ill 												.												hovered                            :                           





                                                                                llI1l1l1                   =                  ll1lll1l 





                                                            else                                :                               





                                                                                llI1l1l1                     =                    II1IIIll 






                                                            if llI1l1l1                           ==                          II1IIIll 												:												






                                                                                if not l1lI1Ill                  .                 is_reachable                                 :                                
                                                                                                    llI1l1l1 									=									Ill11llI 








                                                                                else 													:													

                                                                                                    llI1l1l1 								=								l1llllI1 


                                                            if llI1l1l1                                 ==                                l1llllI1 															:															


                                                                                I11l1llI                          =                         IIllIlI1 









                                                            if llI1l1l1 													==													ll1II1ll                     :                    




                                                                                I11l1llI 									=									l1l1ll1l 

                                                            if I11l1llI 													==													II11IllI                               :                              









                                                                                if not Il11lIll 														.														llIl11II 											(											lIII1III 												)												                        :                        


                                                                                                    I11l1llI 														=														lllII1ll 



                                                                                else 															:															








                                                                                                    I11l1llI 										=										IIl11II1 

                                                            if I11l1llI 												==												I1lllIl1 											:											

                                                                                llIll11l 								=								I1llI11I 








                                                            if I11l1llI                       ==                      llIlIIIl 															:															









                                                                                llIll11l                  =                 Il1I111I 

                                                            if llIll11l 												==												Il1lIlI1                  :                 







                                                                                III1IIII 										=										l1l1l11I 







                                                                                if lIl1I11I 															(															IllIlI1l 																,																l1ll1III 												)												                          :                          









                                                                                                    III1IIII                          =                         II11IIlI 


                                                                                else                      :                     

                                                                                                    III1IIII                       =                      l1lI1II1 

                                                                                if III1IIII                              ==                             IIll11I1                      :                     







                                                                                                    if not Il11lIll 																.																llIl11II                                 (                                IIlIIll1 								)								                           :                           


                                                                                                                        III1IIII                              =                             IIl1Il1l 








                                                                                                    else                       :                      





                                                                                                                        III1IIII                               =                              l1llIll1 

                                                                                if III1IIII 											==											l1lI1II1                    :                   






                                                                                                    llIll11l 										=										Il1I111I 



                                                                                if III1IIII                      ==                     IllllII1 														:														








                                                                                                    llIll11l 								=								l1IllllI 





                                                            if llIll11l                       ==                      lIlIl1ll 															:															
                                                                                l1I1IIl1 									=									l11l1lII 


                                                                                ll11llIl                       =                      l1lIlI1l 



                                                                                if not l1111l1l 										(										l1ll1III                     )                                            :                        

                                                                                                    ll11llIl                               =                              I1l1I11I 

                                                                                else                        :                       

                                                                                                    ll11llIl 															=															l11I1I1l 







                                                                                if ll11llIl                    ==                   II11111I 								:								



                                                                                                    III11lll                               =                              Il111lII 






                                                                                                    if IIII11lI                              (                             IlIlIIlI 												,												IlIlllI1                         )                        													:													








                                                                                                                        III11lll 											=											llI1lIII 






                                                                                                    else                            :                           



                                                                                                                        III11lll 										=										IlIIlIll 

                                                                                                    if III11lll                   ==                  IIIlll11                            :                           



                                                                                                                        if not player                                .                               enabled                   :                  


                                                                                                                                            III11lll 															=															IlIll1l1 



                                                                                                                        else 												:												




                                                                                                                                            III11lll                        =                       IIII1IIl 




                                                                                                    if III11lll                   ==                  l1IllI1I 								:								








                                                                                                                        ll11llIl                               =                              Il11llll 


                                                                                                    if III11lll                   ==                  Ill1I11l 																:																

                                                                                                                        ll11llIl                       =                      l1II1II1 





                                                                                if ll11llIl                                ==                               I1l1I11I                                 :                                

                                                                                                    l1I1IIl1 													=													l11111II 









                                                                                if ll11llIl                           ==                          I1lIl1ll                                 :                                







                                                                                                    l1I1IIl1                   =                  l1llIIll 





                                                                                if l1I1IIl1 								==								l1llIIIl 															:															








                                                                                                    II1I11lI                       =                      lII1IlII 


                                                                                                    if not I1llll11 										(										l11I1I1I 													)													                                :                                






                                                                                                                        II1I11lI                   =                  Il1IllIl 







                                                                                                    else                         :                        


                                                                                                                        II1I11lI 															=															IlIIl1ll 








                                                                                                    if II1I11lI                        ==                       llI1II11 									:									






                                                                                                                        if not I1I1l11l 														:														





                                                                                                                                            II1I11lI                            =                           llI111ll 




                                                                                                                        else 																:																
                                                                                                                                            II1I11lI 									=									lI11ll1I 




                                                                                                    if II1I11lI                     ==                    IlII1l11 															:															






                                                                                                                        l1I1IIl1                                =                               lIl1I11l 

                                                                                                    if II1I11lI                       ==                      I11Il111 											:											
                                                                                                                        l1I1IIl1 									=									IIlIlIlI 




                                                                                if l1I1IIl1                        ==                       I111lIII 											:											






                                                                                                    Il1l1l11 																=																lIII1lIl 




                                                                                                    I11lIlll 								=								IlI1ll1l 







                                                                                                    if not I1llll11                  (                 llIl1I11                                )                                                               :                                



                                                                                                                        I11lIlll                             =                            lI1l11lI 



                                                                                                    else                       :                      



                                                                                                                        I11lIlll 								=								IlI11llI 




                                                                                                    if I11lIlll                                 ==                                llIII1lI 											:											



                                                                                                                        llI11I11 											=											IllIIII1 









                                                                                                                        if not IIII11lI 									(									IlIlIIlI                         ,                        I1l1ll11                               )                              								:								







                                                                                                                                            llI11I11 												=												l11I1IlI 






                                                                                                                        else 														:														









                                                                                                                                            llI11I11                              =                             IIII11ll 


                                                                                                                        if llI11I11 													==													IIl1I1Il                             :                            
                                                                                                                                            if not player                             .                            enabled 									:									





                                                                                                                                                                llI11I11 														=														l11IlI1I 









                                                                                                                                            else                 :                









                                                                                                                                                                llI11I11                              =                             IIIIIlI1 

                                                                                                                        if llI11I11 												==												lIII1III                           :                          



                                                                                                                                            I11lIlll                             =                            IIII1IlI 





                                                                                                                        if llI11I11                             ==                            II1I11ll                               :                              
                                                                                                                                            I11lIlll 												=												l1IllllI 




                                                                                                    if I11lIlll 								==								IllIlI1l 										:										

                                                                                                                        Il1l1l11 												=												IIllIl11 






                                                                                                    if I11lIlll 												==												l1IllllI 														:														

                                                                                                                        Il1l1l11                  =                 I1l1IIIl 








                                                                                                    if Il1l1l11 														==														l1ll1Il1                            :                           



                                                                                                                        l1l1lI11 																=																lIllll11 









                                                                                                                        if not Il11lIll 								.								llIl11II 										(										IIl1llI1                   )                  										:										



                                                                                                                                            l1l1lI11                              =                             IIIlI1lI 




                                                                                                                        else                                :                               

                                                                                                                                            l1l1lI11                              =                             IlllIIl1 





                                                                                                                        if l1l1lI11                    ==                   Ill111l1                      :                     


                                                                                                                                            if not I1llll11 								(								llIIIll1                         )                                                 :                         

                                                                                                                                                                l1l1lI11 												=												l111l1II 







                                                                                                                                            else                             :                            
                                                                                                                                                                l1l1lI11 												=												llIlIIll 

                                                                                                                        if l1l1lI11                               ==                              lIlIlIll 											:											
                                                                                                                                            Il1l1l11 									=									IIlIIll1 







                                                                                                                        if l1l1lI11 													==													l111l1II 										:										




                                                                                                                                            Il1l1l11                         =                        ll11IlI1 







                                                                                                    if Il1l1l11 																==																IlllllI1                      :                     





                                                                                                                        pass 



                                                                                                    if Il1l1l11 											==											IIlIlIlI                       :                      








                                                                                                                        l1lI1Ill 													.													play_destroy_sound 										(																										)																








                                                                                                                        l1lI1Ill                       .                      destroy_block 													(													                            )                            









                                                                                if l1I1IIl1 														==														llII1llI                     :                    


                                                                                                    l1lI1Ill 															.															play_create_sound                     (                    													)													

                                                                                                    l1lI1Ill                               .                              block_dict 															.															get                    (                   block_pick 										)										                  (                  position 														=														l1lI1Ill 										.										position 								+								fuck_up_i 												(												mouse                          .                         normal 																)																                            )                            





                                                            if llIll11l 																==																lIIl1Ill                       :                      



                                                                                pass 









                                        def play_create_sound                               (                              self 								)								                      :                      


                                                            lIlIllI1                            =                           self 






                                                            Il1IIIlI 									.									play 								(																)								





                                        def play_destroy_sound                    (                   self 														)														                      :                      




                                                            IlI1IlIl 								=								self 






                                                            Il1IIIlI                            .                           play                      (                                                 )                            









                                        def destroy_block 															(															self                  )                 											:											





                                                            llII11Il 																=																self 








                                                            I1I11ll1                               =                              I11lIIII 









                                                            Ill1lIIl                              =                             lll1111l 





                                                            if not I1llll11 								(								I1II11l1 									)									                            :                            





                                                                                Ill1lIIl 																=																llI111ll 









                                                            else                               :                              








                                                                                Ill1lIIl                         =                        II11111I 







                                                            if Ill1lIIl                            ==                           III1ll1I 									:									







                                                                                if not l1I1lII1                                :                               





                                                                                                    Ill1lIIl 													=													II1III1I 





                                                                                else                           :                          

                                                                                                    Ill1lIIl 												=												IIlIl1I1 
                                                            if Ill1lIIl 														==														II1III1I 																:																
                                                                                I1I11ll1                   =                  lI11llll 

                                                            if Ill1lIIl                             ==                            I1l1IllI 														:														






                                                                                I1I11ll1 																=																lI1IlI11 


                                                            if I1I11ll1 									==									lIlI11I1                    :                   



                                                                                I1IlII1I                                =                               I11Il111 


                                                                                if not l111I11I 															:															





                                                                                                    I1IlII1I                                =                               IlI1IIII 
                                                                                else 															:															
                                                                                                    I1IlII1I                     =                    l1I1lIlI 








                                                                                if I1IlII1I                     ==                    Il1I1lll                                 :                                








                                                                                                    if not llII11Il                  .                 is_destroyed 										:										






                                                                                                                        I1IlII1I 														=														Il111lII 









                                                                                                    else 												:												









                                                                                                                        I1IlII1I 																=																Il111ll1 

                                                                                if I1IlII1I 									==									lll11IIl 											:											








                                                                                                    I1I11ll1                    =                   ll1111lI 








                                                                                if I1IlII1I                     ==                    Il111lII 															:															




                                                                                                    I1I11ll1 												=												lIIlIl1l 


                                                            if I1I11ll1 																==																ll1111lI                            :                           









                                                                                pass 

                                                            if I1I11ll1 											==											II1l1lI1 														:														









                                                                                llII11Il 												.												is_destroyed                         =                        fuck_up                                (                               l1IIlII1 															)															






                                                                                destroy                               (                              llII11Il 														)														




                                                                                lllI1II1 															.															remove 																(																llII11Il 																)																









                                        @                      IIlI11l1 


                                        def force_destroy                              (                             self                            )                           													:													





                                                            lll1I111                               =                              self 







                                                            destroy                    (                   lll1I111 									)									








                                                            lllI1II1 																.																remove                  (                 lll1I111 																)																
                    IlIlIl11 





                    class BlockItemEntity 									(									Entity                                 )                                										:										










                                        def __init__ 											(											self 									,									texture 															,															original_block                               :                              str 															,															position                    =                                   (                IIIl111I 													,													Ill1II1l 										,										Ill1II1l 															)															                   )                   										:										






                                                            (													l111lllI 															,															IIIl111l 																,																l1Il1lll                    ,                   Il1lIllI                        )                                                  =                           												(												self                               ,                              position 													,													texture                             ,                            original_block 														)														







                                                            super 										(																						)												                           .                           __init__                           (                          parent                 =                scene                        ,                       position                               =                              IIIl111l 													,													model                          =                         II1llIlI                                ,                               origin_y                               =                              lllllIll 															,															texture                              =                             l1Il1lll                    ,                   scale 															=															l111111I                                 )                                




                                                            l111lllI 																.																collider                         =                        BoxCollider 									(									l111lllI                              )                             









                                                            l111lllI 											.											block 											=											Il1lIllI 






                                                            l111lllI 													.													velocity_y                       =                      Ill1II1l 







                                                            l111lllI 									.									gravity                                 =                                                 -                 l1llIl1l 

                                        def update                                 (                                self                            )                           																:																









                                                            lI1I1IlI 												=												self 







                                                            lI1I1IlI                          .                         velocity_y 															+=															lI1I1IlI                           .                          gravity                     *                    time                           .                          dt 








                                                            I1I1IlI1                   =                  lI1I1IlI 										.										y                 +                lI1I1IlI                        .                       velocity_y 											*											time 														.														dt 



                                                            llllIlll 										=										ll1lll1l 









                                                            IIlI11I1 														=														llI1Il1l 




                                                            if not I1llll11                                 (                                III1111l 											)																										:															









                                                                                IIlI11I1 																=																II111lIl 
                                                            else                 :                







                                                                                IIlI11I1 																=																Il1lIlI1 





                                                            if IIlI11I1                           ==                          II111lIl 								:								






                                                                                if not I1llll11                               (                              lIII111l                                )                                                  :                   



                                                                                                    IIlI11I1                           =                          lll1IIll 
                                                                                else 														:														


                                                                                                    IIlI11I1                           =                          III1IlII 





                                                            if IIlI11I1 									==									Il1lIlI1                                 :                                



                                                                                llllIlll 									=									II1III1I 





                                                            if IIlI11I1 											==											III1IlII 											:											







                                                                                llllIlll                           =                          l1l111l1 






                                                            if llllIlll 														==														I1l1III1                    :                   







                                                                                IIlll1Il                                 =                                Il111IIl 





                                                                                if not II11111I                   :                  


                                                                                                    IIlll1Il 																=																l11lIlII 






                                                                                else                     :                    
                                                                                                    IIlll1Il                               =                              l1lll1II 









                                                                                if IIlll1Il                          ==                         l11l1lII 											:											





                                                                                                    if not lI1I1IlI                        .                       detect_collision 														(														I1I1IlI1 															)															                         :                         







                                                                                                                        IIlll1Il                        =                       lII1lIlI 









                                                                                                    else 									:									


                                                                                                                        IIlll1Il                           =                          I1IlIIll 






                                                                                if IIlll1Il 											==											Il11l111 																:																








                                                                                                    llllIlll 								=								I111l111 






                                                                                if IIlll1Il                      ==                     IlIlIll1 										:										









                                                                                                    llllIlll                          =                         lII1lIlI 

                                                            if llllIlll 										==										I1lll11I 											:											



                                                                                lI1I1IlI 																.																velocity_y 																=																Ill1II1l 









                                                            if llllIlll                       ==                      IlIlIll1                    :                   

                                                                                lI1I1IlI 								.								y                              =                             I1I1IlI1 

                                                            lI1I1IlI                     .                    rotation_y 										+=										IIll11I1 










                                        def detect_collision                               (                              self 									,									potential_y 										)										                   :                   

                                                            (										IlII11II                 ,                IlIlllIl                 )                								=								                        (                        potential_y                               ,                              self 																)																


                                                            IIII1Il1 											=											Vec3 														(														IlIlllIl                 .                x 										,										IlII11II                     ,                    IlIlllIl                      .                     z                         )                        








                                                            IlIlllIl                                 .                                collider 												=												BoxCollider                            (                           IlIlllIl                              )                             





                                                            IllIlI1I 													=													IlIlllIl 														.														intersects 														(																											)													
                                                            I1l1lIIl 										=										lIlI1II1 


                                                            IlIll11l                             =                            ll1l1I11 




                                                            if not lI11I1l1 																(																I111l1II 								,								lIIl1Ill                   )                                       :                     







                                                                                IlIll11l                      =                     IIl11II1 






                                                            else 												:												







                                                                                IlIll11l 												=												l1I1lII1 
                                                            if IlIll11l                             ==                            ll1III1I 																:																
                                                                                if not IllIlI1I 											.											hit 								:								



                                                                                                    IlIll11l                 =                lIlI11I1 







                                                                                else 																:																


                                                                                                    IlIll11l                                 =                                l11I1IlI 








                                                            if IlIll11l 										==										I1l1II1l 											:											




                                                                                I1l1lIIl 											=											l1lI1II1 




                                                            if IlIll11l 											==											IIl11lll 															:															




                                                                                I1l1lIIl                        =                       IIIlI1lI 






                                                            if I1l1lIIl 										==										Il1l11I1                             :                            





                                                                                IIl1lll1                         =                        l1Il1llI 



                                                                                if not I1I11IIl                 :                

                                                                                                    IIl1lll1 											=											Il11llll 







                                                                                else                                 :                                






                                                                                                    IIl1lll1                      =                     l11111Il 





                                                                                if IIl1lll1                  ==                 lIl1I11l 												:												








                                                                                                    if not I1llll11 															(															lIl1lII1 																)																										:										

                                                                                                                        IIl1lll1 										=										Il11llll 









                                                                                                    else 										:										







                                                                                                                        IIl1lll1                                =                               Illl1III 


                                                                                if IIl1lll1                               ==                              IllI1l11 								:								



                                                                                                    I1l1lIIl 															=															IIl1Il1l 
                                                                                if IIl1lll1 														==														I1l1lIll 																:																

                                                                                                    I1l1lIIl 															=															l111I1I1 



                                                            if I1l1lIIl 												==												Illl11II 															:															




                                                                                pass 






                                                            if I1l1lIIl 												==												lll1I1II                               :                              


                                                                                return fuck_up                                 (                                lllI1111 															)															




                                                            return fuck_up                   (                  llllIlIl                     )                    


                    class GrassBlock 														(														Block 									)									                                :                                








                                        def __init__ 								(								self                             ,                            position                      =                     															(															l1IIII1I                     ,                    IIIl111I 								,								ll1l11II                                 )                                											)																								:													


                                                            (													l11ll111 									,									II1lIlIl 										)										                            =                            								(								self 											,											position 															)															



                                                            super                    (                   								)								                         .                         __init__ 									(									texture 												=												I1lIIl1l                         ,                        position 															=															II1lIlIl 																)																





                    class StoneBlock 														(														Block                             )                                            :                






                                        def __init__ 															(															self                               ,                              position 																=																                     (                     ll1l11II 													,													ll1l11II 														,														lIl11III                      )                     													)													                                :                                
                                                            (													lll1ll11                            ,                           llI1ll1l 									)																									=																                            (                            position                       ,                      self                           )                          


                                                            super                           (                                                   )                         															.															__init__                     (                    texture 															=															lI1lI1I1                      ,                     position 												=												lll1ll11                    )                   



                    class BrickBlock                      (                     Block                            )                           										:										

                                        def __init__                         (                        self                    ,                   position                            =                                                        (                             l1IIII1I 								,								ll1l11II                              ,                             ll1l11II                 )                														)														                                :                                


                                                            (								I1I11l1l 													,													I1lll1Il                           )                          											=											                         (                         self 										,										position 												)												





                                                            super 									(																				)																											.																__init__ 															(															texture                        =                       ll1111l1 												,												position                                 =                                I1lll1Il                        )                       

                    class DirtBlock                   (                  Block                        )                       									:									




                                        def __init__                      (                     self                          ,                         position                      =                     															(															ll1l11II 											,											l1IIII1I                           ,                          II11lI1I 												)																							)											                           :                           
                                                            (                              IIlII1lI 											,											II1lIlII                 )                														=														                          (                          position                        ,                       self 																)																









                                                            super 																(																                        )                                                 .                         __init__ 								(								texture 									=									llII1l1l                           ,                          position                                =                               IIlII1lI                          )                         



                    class BedrockBlock                     (                    Block                            )                           																:																



                                        def __init__                   (                  self                      ,                     position                 =                														(														lIl11III                              ,                             Ill1II1l 														,														l1IIII1I                     )                    													)																									:												


                                                            (                        IlIlI11l 											,											l11I1I11                                 )                                                  =                  												(												self 												,												position 														)														






                                                            super                             (                                                          )                              										.										__init__ 															(															texture                   =                  random                           .                          choice 												(												textures                   )                                            ,                          position 									=									l11I1I11                            )                           









                                        def destroy_block                                (                               self 															)																														:															
                                                            l11IIIlI 															=															self 
                                                            pass 









                    class GlassBlock                      (                     Block                              )                             								:								









                                        def __init__                                (                               self                    ,                   position 										=																		(								IIIl111I 									,									ll1l11II 								,								ll1l11II                                 )                                                   )                                                  :                               





                                                            (								lII1I1I1                            ,                           IIl1Ill1 																)																												=												                 (                 self                           ,                          position 												)												







                                                            super                                 (                                                )                                                .                                __init__                      (                     texture 											=											l1I1llII 								,								position                              =                             IIl1Ill1 													)													



                                        def play_destroy_sound                       (                      self                             )                            										:										






                                                            IlIIIl1I                                =                               self 






                                                            II1111lI                          .                         play                         (                        									)									




                    class BasicWoodBlock 														(														Block 													)																					:								

                                        def __init__                          (                         self                            ,                           position 												=												                       (                       ll1l11II 														,														ll1l11II 																,																IIIl111I 												)												                )                											:											





                                                            (                 l11IIlIl                        ,                       l111IIll                              )                             								=								                   (                   position                           ,                          self                               )                              







                                                            super                       (                                                    )                                                       .                         __init__ 												(												texture 														=														lI1ll111                     ,                    position 																=																l11IIlIl                   )                  



                    class BasicWoodBlockPlanks                   (                  Block 																)																										:										



                                        def __init__                  (                 self                         ,                        position 									=																			(										ll1l11II                          ,                         lIl11III 									,									ll1l11II                        )                       											)																					:										


                                                            (                l11IlIII                             ,                            l11Il1I1                      )                     											=																								(													position                        ,                       self                             )                            



                                                            super                       (                                                  )                            																.																__init__ 																(																texture                                =                               llIIIIll 															,															position 												=												l11IlIII 												)												
                                                            l11Il1I1 																.																model                   =                  random                                 .                                choice                   (                  objects 															)															







                    class DEBUG_CHOCOLATE_CAKE_BLOCK 												(												Block                        )                                                     :                              



                                        def __init__ 												(												self                               ,                              position                        =                       										(										II11lI1I                            ,                           l1IIII1I 								,								l1IIII1I 														)														                               )                               									:									






                                                            (                         llI1Illl 										,										IlIIIllI 								)																					=																										(													position                          ,                         self                           )                          




                                                            super                        (                       												)												                      .                      __init__ 								(								texture 														=														I1I11II1                      ,                     position                  =                 llI1Illl                 )                


                    global save_world 



                    def save_world 																(																                         )                         										:										


                                        with lI1Il11l 								(								lII1II11                   .                  format                                (                               lIIIlI11 											)																									,														I11III1l                            )                           as I1lIIlII                                :                               



                                                            while 															(															                                (                                l1IIIll1 and I1llll11 															(															I1IlIIll 								)								                               )                               and                  (                 Il11lIll                     .                    llIl11II                        (                       I1l1ll11 														)														and Il11lIll                    .                   llIl11II 													(													lIIll1II 								)																							)															                               )                               and                        (                       I1llll11                 (                IIIlll11                      )                     and I1llll11                           (                          l11Il1l1                            )                           or 											(											not I1llll11 													(													I111l1lI 																)																or not l1111l1l 																(																lIlI1II1 											)											                                )                                									)																			:										






                                                                                while 														(														I1llll11                  (                 Il11Ill1 													)													and lIIl1Ill or                        (                       l1111l1l 												(												lIl1l1lI 									)									and 											(											not I11IIIll 								)																			)																										)															and                                (                               not lI1Il1ll and I1llll11                      (                     IIllIlIl                         )                        or 																(																I1III1ll 													>													llI11llI and Il11lIll                                .                               llIl11II                   (                  II1I1111                      )                     															)																													)																														:																



                                                                                                    for                       (                      lll111l1                               ,                              llll11Il                   )                  in l1IlIIl1 									(									lllI1II1                    ,                   l11111ll                      )                     														:														




                                                                                                                        l1IIIllI                          =                         IIlIlIlI 

                                                                                                                        l111l1l1 									=									lIllllII 







                                                                                                                        if not IIII11lI                        (                       II1l1lI1 								,								l1l1Il1l                                 )                                																:																

                                                                                                                                            l111l1l1 													=													IllI1IIl 






                                                                                                                        else 														:														




                                                                                                                                            l111l1l1 												=												lIllll11 

                                                                                                                        if l111l1l1                         ==                        IlllllI1                               :                              









                                                                                                                                            if not l1111l1l                           (                          ll1111lI 												)																							:											





                                                                                                                                                                l111l1l1 														=														lIll1I1l 






                                                                                                                                            else                      :                     



                                                                                                                                                                l111l1l1                                =                               Illl1I11 








                                                                                                                        if l111l1l1                               ==                              I1l11lll 															:															

                                                                                                                                            l1IIIllI 															=															IlI1IIII 




                                                                                                                        if l111l1l1 								==								IIlIIl1l                   :                  







                                                                                                                                            l1IIIllI 											=											l11l1I11 








                                                                                                                        if l1IIIllI                               ==                              IlI1II1l                                :                               







                                                                                                                                            III11Ill 											=											l1ll1llI 







                                                                                                                                            if not II1lIIll                               :                              
                                                                                                                                                                III11Ill 												=												I1l1IllI 





                                                                                                                                            else 												:												
                                                                                                                                                                III11Ill 									=									l1llllI1 








                                                                                                                                            if III11Ill 													==													lIl1IIIl                              :                             

                                                                                                                                                                lIIlII11                            =                           llI1lIII 









                                                                                                                                                                lIIIIIll                 =                II111I1I 

                                                                                                                                                                I111lI11                 =                llI1II11 






                                                                                                                                                                if not IlIIII1l                               (                              lIlll1I1 															,															Il1I1lll                          )                         													:													

                                                                                                                                                                                    I111lI11 														=														l11lI1lI 







                                                                                                                                                                else 											:											


                                                                                                                                                                                    I111lI11 														=														lllI1l1l 
                                                                                                                                                                if I111lI11                   ==                  l1I11IlI                            :                           








                                                                                                                                                                                    if not Il11lIll                           .                          llIl11II 										(										llI1lIII 														)														                :                



                                                                                                                                                                                                        I111lI11 														=														I1l1lIll 







                                                                                                                                                                                    else                          :                         
                                                                                                                                                                                                        I111lI11 										=										lI1Il1ll 









                                                                                                                                                                if I111lI11                         ==                        llIIlI1I 								:								




                                                                                                                                                                                    lIIIIIll                       =                      IlllI1lI 
                                                                                                                                                                if I111lI11 																==																Illl1III                               :                              

                                                                                                                                                                                    lIIIIIll                   =                  llll11II 

                                                                                                                                                                if lIIIIIll                      ==                     ll1Ill11 													:													







                                                                                                                                                                                    lll1I1I1                                 =                                IIl1l11I 









                                                                                                                                                                                    if not lI11I1l1 												(												II11111I 															,															lI1IIIlI                                 )                                                      :                      




                                                                                                                                                                                                        lll1I1I1 														=														Ill1I11I 


                                                                                                                                                                                    else                  :                 

                                                                                                                                                                                                        lll1I1I1 															=															llI1lIII 




                                                                                                                                                                                    if lll1I1I1 											==											l1IIllI1                          :                         









                                                                                                                                                                                                        if not I1llll11                     (                    llllI11I 										)																				:										





                                                                                                                                                                                                                            lll1I1I1                   =                  IIl11II1 






                                                                                                                                                                                                        else 															:															

                                                                                                                                                                                                                            lll1I1I1 											=											l11l1lII 





                                                                                                                                                                                    if lll1I1I1                  ==                 l11lI1lI 								:								









                                                                                                                                                                                                        lIIIIIll 														=														Illl11II 







                                                                                                                                                                                    if lll1I1I1                       ==                      IIl11II1                     :                    


                                                                                                                                                                                                        lIIIIIll 												=												lIIIl11l 




                                                                                                                                                                if lIIIIIll 													==													l1lI1II1                                :                               
                                                                                                                                                                                    lIIlII11 															=															IlII1l11 


                                                                                                                                                                if lIIIIIll                      ==                     llll11II 								:								







                                                                                                                                                                                    lIIlII11 								=								Il1llII1 







                                                                                                                                                                if lIIlII11                        ==                       IlII1l11 																:																



                                                                                                                                                                                    II1I1III 									=									l1IllI1l 






                                                                                                                                                                                    I1Il111I                             =                            lIllIl11 






                                                                                                                                                                                    if not lIl1I11I                           (                          IIlIlIlI                     ,                    I11I1IlI                             )                                              :                  


                                                                                                                                                                                                        I1Il111I 										=										lIII1lIl 









                                                                                                                                                                                    else 													:													





                                                                                                                                                                                                        I1Il111I                                 =                                III1ll1I 


                                                                                                                                                                                    if I1Il111I 													==													lIIIl11l 													:													







                                                                                                                                                                                                        if not lII11l1I                              :                             






                                                                                                                                                                                                                            I1Il111I                 =                l11I1Ill 






                                                                                                                                                                                                        else 											:											








                                                                                                                                                                                                                            I1Il111I 								=								l11I1I1l 





                                                                                                                                                                                    if I1Il111I                                ==                               l11I1Ill                       :                      


                                                                                                                                                                                                        II1I1III                    =                   Il11I111 

                                                                                                                                                                                    if I1Il111I                                ==                               II11111I                                 :                                



                                                                                                                                                                                                        II1I1III                             =                            IIl1l11I 








                                                                                                                                                                                    if II1I1III                            ==                           lIIl1lI1 													:													
                                                                                                                                                                                                        llIll11I 									=									I1l1llII 



                                                                                                                                                                                                        if not l1111l1l 												(												IIl111I1                        )                       								:								


                                                                                                                                                                                                                            llIll11I                                =                               llIIIll1 

                                                                                                                                                                                                        else 														:														







                                                                                                                                                                                                                            llIll11I 									=									l1l1ll1I 



                                                                                                                                                                                                        if llIll11I                           ==                          l1l1ll1I                  :                 



                                                                                                                                                                                                                            if not l1lll1II 								:								






                                                                                                                                                                                                                                                llIll11I 													=													llIlIIll 
                                                                                                                                                                                                                            else 														:														



                                                                                                                                                                                                                                                llIll11I                            =                           l1II1llI 



                                                                                                                                                                                                        if llIll11I 									==									l1llIIll 												:												







                                                                                                                                                                                                                            II1I1III                            =                           lIllllll 





                                                                                                                                                                                                        if llIll11I                   ==                  l1ll1llI 											:											
                                                                                                                                                                                                                            II1I1III 																=																l11111Il 


                                                                                                                                                                                    if II1I1III 																==																l1II1llI                          :                         





                                                                                                                                                                                                        lIIlII11 									=									Il1llII1 







                                                                                                                                                                                    if II1I1III 													==													lIllllll                        :                       



                                                                                                                                                                                                        lIIlII11 									=									Ill111l1 





                                                                                                                                                                if lIIlII11                             ==                            llIIIll1 													:													





                                                                                                                                                                                    III11Ill                        =                       l11I1IlI 


                                                                                                                                                                if lIIlII11 														==														IIlIlIlI 											:											

                                                                                                                                                                                    III11Ill 										=										IIlIl1I1 


                                                                                                                                            if III11Ill 												==												IIlIl1I1                           :                          






                                                                                                                                                                l1IIIllI 														=														l11l1I11 









                                                                                                                                            if III11Ill 														==														IIl11lll                          :                         
                                                                                                                                                                l1IIIllI                                 =                                lIllllll 








                                                                                                                        if l1IIIllI                          ==                         lIIl11II 															:															




                                                                                                                                            pass 
                                                                                                                        if l1IIIllI 										==										lIIll1II                  :                 




                                                                                                                                            I1lIIlII                       .                      write 								(								f'{llll11Il.position}:{l1Il1I1I(llll11Il).__name__}\n'                             )                             







                                                                                                                                            escmenu                        .                       showStateText 										(										lIIII1l1 										)										



                                                                                                    break 
                                                                                break 

                    def load_world 								(																							)																													:														



                                        try 														:														






                                                            l1lI11II 															=																															{																lIl1II11 													:													GrassBlock                         ,                        I1lIIIlI 												:												StoneBlock                  ,                 l1lllIlI                             :                            BrickBlock 																,																II1I11l1                   :                  DirtBlock                               ,                              IlI1lII1                             :                            BedrockBlock 										,										ll1Il1lI                         :                        GlassBlock 															,															I11IIll1                     :                    BasicWoodBlock 														,														llll1I11 															:															BasicWoodBlockPlanks                               }                              

                                                            with lI1Il11l 												(												f'{lIIIlI11}/world.pcw'                           ,                           ll1ll1Il 											)											as llIl1III                      :                     







                                                                                l1llI1I1 										=										llIl1III 								.								readlines                          (                                                       )                              





                                                                                II11111l                        =                       IlII111l                             (                            l1llI1I1 														)														








                                                                                for ll11lll1 in 															[															llI1l1II 															]																												:													




                                                                                                    if 								(																								(																I1IIlIIl                  !=                 l1l1l11I or l1111l1l 								(								l11111Il                    )                                              )                           or                        (                       not Il11lIll                       .                      llIl11II                               (                              l1111Ill                    )                   or not l1111l1l                                 (                                l1I1Il11 									)																					)												                             )                             and                              (                                                 (                    Il11lIll 															.															llIl11II 														(														l1llIIl1 															)															and I1llll11                    (                   IlI11lIl 																)																                       )                       and 																(																IIl1l111                  ==                 IlIIl1I1 and Il11I111                           !=                          Il11llI1 											)											                           )                                                     :                          


                                                                                                                        while                              (                                                     (                        l1111l1l                                (                               l1I1I11I 												)												and lIII1lIl 									)									and                 (                not I1l1llII or I1llll11                                (                               Illl1II1 									)																									)																                           )                           and 															(															                (                lI1l1lI1 														>=														ll1Ill11 or not l1111l1l 									(									lllllIll                           )                          											)											and 															(															l1111l1l 														(														II1IIIll 													)													and l1111l1l                           (                          Illl1II1                        )                                        )                                              )                             								:								








                                                                                                                                            while                        (                       Il11lIll 															.															llIl11II                              (                             lIl1IIIl 															)															and I1l1II1l                  <                 l1I11ll1 or 													(													not II1III1I or not l1111l1l 									(									Illl1I11                               )                                                          )                                                     )                         or                            (                           															(															lI11llll and l1111l1l                              (                             II1IlI1l 												)																												)																and 											(											not Illl1I11 or not Il11lIll                 .                llIl11II 									(									IIlIl11l                          )                                                         )                                                               )                                                     :                      


                                                                                                                                                                for 													(													I1lIll1I                           ,                          lII11llI                         )                        in l1IlIIl1 														(														l1llI1I1                     ,                    start                    =                   lIl11III 												)																							:											




                                                                                                                                                                                    I1Il1II1                           =                          IIllIlI1 



                                                                                                                                                                                    l1l1lll1 															=															IIl1I1Il 






                                                                                                                                                                                    IIIIllIl 								=								IIII11ll 





                                                                                                                                                                                    I1ll1II1 											=											l1lllllI 
                                                                                                                                                                                    llIlllI1 																=																Ill1I11l 






                                                                                                                                                                                    if not II11Illl                            :                           







                                                                                                                                                                                                        llIlllI1 								=								IlllllI1 







                                                                                                                                                                                    else 												:												



                                                                                                                                                                                                        llIlllI1 												=												Illl1III 





                                                                                                                                                                                    if llIlllI1 															==															Illl1III 													:													








                                                                                                                                                                                                        if not l1111l1l                    (                   lII11l1I                                 )                                													:													



                                                                                                                                                                                                                            llIlllI1 										=										IlI11llI 




                                                                                                                                                                                                        else 															:															



                                                                                                                                                                                                                            llIlllI1                        =                       lIllll11 






                                                                                                                                                                                    if llIlllI1                         ==                        IlI11llI                        :                       




                                                                                                                                                                                                        I1ll1II1 															=															lIlIl1ll 




                                                                                                                                                                                    if llIlllI1                 ==                IlllllI1                             :                            

                                                                                                                                                                                                        I1ll1II1 												=												l111lII1 


                                                                                                                                                                                    if I1ll1II1                             ==                            II1IIlll                               :                              




                                                                                                                                                                                                        lllII11l 								=								Il111lII 
                                                                                                                                                                                                        if not Il11lIll                    .                   llIl11II 														(														I11lII11                            )                                              :                   




                                                                                                                                                                                                                            lllII11l                               =                              I1llll1l 






                                                                                                                                                                                                        else                            :                           


                                                                                                                                                                                                                            lllII11l                    =                   lII1lIlI 


                                                                                                                                                                                                        if lllII11l 															==															I1l11lll                 :                








                                                                                                                                                                                                                            if not l1111l1l 									(									l1IIl1ll                                 )                                                            :                            



                                                                                                                                                                                                                                                lllII11l 													=													I1l1I111 





                                                                                                                                                                                                                            else 									:									

                                                                                                                                                                                                                                                lllII11l 								=								IIlIIll1 
                                                                                                                                                                                                        if lllII11l 																==																IlIlIll1                      :                     



                                                                                                                                                                                                                            I1ll1II1                          =                         IIlIIll1 

                                                                                                                                                                                                        if lllII11l                  ==                 IIlIIll1                                 :                                

                                                                                                                                                                                                                            I1ll1II1 														=														IIl1l11I 









                                                                                                                                                                                    if I1ll1II1                      ==                     IIl1l11I 															:															









                                                                                                                                                                                                        IIIIllIl 																=																l1l1lllI 









                                                                                                                                                                                    if I1ll1II1                     ==                    IIllIl11                           :                          


                                                                                                                                                                                                        IIIIllIl                     =                    Il1l11I1 




                                                                                                                                                                                    if IIIIllIl 														==														Il1l11I1 									:									




                                                                                                                                                                                                        l11l1lI1 											=											IlI11ll1 



                                                                                                                                                                                                        lll1I1ll                        =                       Ill111l1 








                                                                                                                                                                                                        if not I1llll11                   (                  ll1Ill1l                 )                																:																







                                                                                                                                                                                                                            lll1I1ll 										=										I1l1IllI 









                                                                                                                                                                                                        else                             :                            







                                                                                                                                                                                                                            lll1I1ll 											=											llIlIIIl 




                                                                                                                                                                                                        if lll1I1ll                          ==                         llIlIIIl 										:										



                                                                                                                                                                                                                            if not Il1lIl1l                        :                       


                                                                                                                                                                                                                                                lll1I1ll                     =                    I1l1IllI 





                                                                                                                                                                                                                            else                            :                           



                                                                                                                                                                                                                                                lll1I1ll 											=											Il111lII 


                                                                                                                                                                                                        if lll1I1ll                             ==                            Ill1lI1l 															:															








                                                                                                                                                                                                                            l11l1lI1 								=								II1l1Il1 
                                                                                                                                                                                                        if lll1I1ll 															==															IlIlllII 													:													






                                                                                                                                                                                                                            l11l1lI1                        =                       IlI11llI 







                                                                                                                                                                                                        if l11l1lI1                  ==                 II111I1I                                :                               


                                                                                                                                                                                                                            I1I11l1I 													=													lll1l1ll 
                                                                                                                                                                                                                            if not Il11lIll 								.								llIl11II 												(												II1llllI 													)													                             :                             







                                                                                                                                                                                                                                                I1I11l1I                         =                        l1111llI 



                                                                                                                                                                                                                            else                               :                              

                                                                                                                                                                                                                                                I1I11l1I 									=									I1I1l11l 





                                                                                                                                                                                                                            if I1I11l1I                           ==                          I1lIl1ll 										:										








                                                                                                                                                                                                                                                if llllIIII 											(											II1Il1ll 								,								lIIlIl1l 															)															                                :                                
                                                                                                                                                                                                                                                                    I1I11l1I                  =                 IlI1ll1l 



                                                                                                                                                                                                                                                else 										:										








                                                                                                                                                                                                                                                                    I1I11l1I                      =                     Il11l111 







                                                                                                                                                                                                                            if I1I11l1I                         ==                        I11lIIII                             :                            






                                                                                                                                                                                                                                                l11l1lI1                            =                           I111lIII 




                                                                                                                                                                                                                            if I1I11l1I                            ==                           l1111llI                      :                     





                                                                                                                                                                                                                                                l11l1lI1 												=												lllIIlll 

                                                                                                                                                                                                        if l11l1lI1 												==												Il11I111 											:											









                                                                                                                                                                                                                            IIIIllIl 									=									IIl1llI1 



                                                                                                                                                                                                        if l11l1lI1 													==													IlIIlIll                      :                     








                                                                                                                                                                                                                            IIIIllIl                        =                       IllllII1 






                                                                                                                                                                                    if IIIIllIl 														==														llIll111                                 :                                









                                                                                                                                                                                                        l1l1lll1 															=															l1111llI 



                                                                                                                                                                                    if IIIIllIl 													==													l1llIll1 													:													





                                                                                                                                                                                                        l1l1lll1 											=											lIlI1ll1 


                                                                                                                                                                                    if l1l1lll1                               ==                              l1lI1IIl                    :                   



                                                                                                                                                                                                        if not I1llll11                               (                              IIIl1lI1                                 )                                									:									




                                                                                                                                                                                                                            l1l1lll1                               =                              ll11lllI 









                                                                                                                                                                                                        else 											:											









                                                                                                                                                                                                                            l1l1lll1                            =                           I1l1ll1I 



                                                                                                                                                                                    if l1l1lll1 																==																llI1l1II                              :                             







                                                                                                                                                                                                        I1Il1II1                           =                          l1l1IlIl 

                                                                                                                                                                                    if l1l1lll1 											==											Illl1II1                           :                          









                                                                                                                                                                                                        I1Il1II1                        =                       III1111l 
                                                                                                                                                                                    if I1Il1II1 									==									IlIll1l1                 :                









                                                                                                                                                                                                        lI11lIII 										=										lIll1I1l 






                                                                                                                                                                                                        if not l1111l1l 								(								lll1I1II 															)																								:									
                                                                                                                                                                                                                            lI11lIII                                 =                                l11I1I1l 

                                                                                                                                                                                                        else 															:															
                                                                                                                                                                                                                            lI11lIII 															=															IIlIIll1 
                                                                                                                                                                                                        if lI11lIII                        ==                       II11111I                  :                 





                                                                                                                                                                                                                            if IIII11lI                           (                          I1l1IIIl 												,												Il11lI1l 								)																								:																







                                                                                                                                                                                                                                                lI11lIII 								=								I11lIIII 





                                                                                                                                                                                                                            else                      :                     


                                                                                                                                                                                                                                                lI11lIII                         =                        l1l1II1I 








                                                                                                                                                                                                        if lI11lIII 															==															IIllIl11 															:															









                                                                                                                                                                                                                            I1Il1II1                   =                  I1l1llII 


                                                                                                                                                                                                        if lI11lIII                     ==                    IlI1ll1l                             :                            






                                                                                                                                                                                                                            I1Il1II1 												=												l1l1IlIl 





                                                                                                                                                                                    if I1Il1II1 									==									ll1l1II1 																:																






                                                                                                                                                                                                        lII11llI                       =                      lII11llI                            .                           strip                  (                                               )                              





                                                                                                                                                                                                        IIlIlIll 									=									I1I1llI1 

                                                                                                                                                                                                        lII11I1l                      =                     I1lllIIl 


                                                                                                                                                                                                        if not lII11llI 														:														




                                                                                                                                                                                                                            lII11I1l                               =                              lI11llll 


                                                                                                                                                                                                        else                    :                   








                                                                                                                                                                                                                            lII11I1l 														=														lIl1lII1 









                                                                                                                                                                                                        if lII11I1l                        ==                       IIlllIll 								:								



                                                                                                                                                                                                                            if not l1111l1l 															(															IIll11I1                           )                          																:																








                                                                                                                                                                                                                                                lII11I1l                                =                               II1l1lI1 





                                                                                                                                                                                                                            else                  :                 

                                                                                                                                                                                                                                                lII11I1l                             =                            Il111lII 







                                                                                                                                                                                                        if lII11I1l                            ==                           lI11llll 									:									




                                                                                                                                                                                                                            IIlIlIll                             =                            I1l1IIIl 



                                                                                                                                                                                                        if lII11I1l                          ==                         lIl11llI 																:																









                                                                                                                                                                                                                            IIlIlIll 									=									l1I1lIlI 



                                                                                                                                                                                                        if IIlIlIll                     ==                    l111I11I                      :                     






                                                                                                                                                                                                                            lIl1llIl                    =                   II1III1I 






                                                                                                                                                                                                                            if not llllIIII 									(									lI11llll                         ,                        Illlll1l 												)																							:											








                                                                                                                                                                                                                                                lIl1llIl                               =                              I1I1llI1 
                                                                                                                                                                                                                            else                             :                            


                                                                                                                                                                                                                                                lIl1llIl                              =                             IllIlII1 



                                                                                                                                                                                                                            if lIl1llIl                     ==                    lIlIl1ll                               :                              








                                                                                                                                                                                                                                                if not lI11I1l1                               (                              ll11IlIl 								,								I11IIlIl 												)												                       :                       



                                                                                                                                                                                                                                                                    lIl1llIl 																=																l1I11IlI 








                                                                                                                                                                                                                                                else                        :                       






                                                                                                                                                                                                                                                                    lIl1llIl                   =                  lllI1ll1 







                                                                                                                                                                                                                            if lIl1llIl                                 ==                                lllI1ll1                     :                    
                                                                                                                                                                                                                                                IIlIlIll 								=								l1l1II1I 

                                                                                                                                                                                                                            if lIl1llIl                             ==                            l1I11IlI                    :                   







                                                                                                                                                                                                                                                IIlIlIll                                =                               I1llI11I 








                                                                                                                                                                                                        if IIlIlIll 												==												IlllllI1                  :                 


                                                                                                                                                                                                                            pass 

                                                                                                                                                                                                        if IIlIlIll                     ==                    II1llllI                       :                      
                                                                                                                                                                                                                            (                            IlllIlIl                               ,                              lIl11I11                               )                                              =                lII11llI 													.													split 												(												IlI1lIIl 												)												









                                                                                                                                                                                                                            IlllIlIl                                =                               l1111III                            (                           IIl1lllI                    (                   I1IIII1I                    ,                   IlllIlIl 										.										replace                             (                            l1l1Illl 											,											I1l1Il11 										)																						.												replace 											(											l1I1l1lI 															,															IIlIIII1 										)																				.										split 														(														ll111I1l                                 )                                                 )                 																)																


                                                                                                                                                                                                                            I11lIll1                           =                          l1lI11II 											.											get                         (                        lIl11I11 									,									DEBUG_CHOCOLATE_CAKE_BLOCK 															)															







                                                                                                                                                                                                                            I11lIll1 												(												position                          =                         IlllIlIl                  )                 

                                                                                                                                                                                    if I1Il1II1                                 ==                                l1l1IlIl 									:									








                                                                                                                                                                                                        pass 








                                                                                                                                                                break 





                                                                                                                                            break 









                                        except FileNotFoundError                   :                  



                                                            I1l1I1I1 



                                                            l1I1lI1I 														(														llI1l11l                   )                  
                                                            PyneQuit 										(										II11IIlI                            )                           



                    class EscMenu 													(													Entity 														)														                   :                   






                                        def __init__                        (                       self 																)																                        :                        
                                                            II1l1I11                           =                          self 

                                                            super 														(																						)																					.													__init__ 													(													enabled                               =                              fuck_up                  (                 l1IIlII1 												)												                                ,                                color                           =                          color 																.																hsv 											(											lIl11III 									,									lIl11III                         ,                        II1lI1l1 													,													lIlIlll1 													)													                          ,                          scale 								=								                 (                 window 									.									aspect_ratio 										,										I11IIIll                    )                   												,												position                    =                                                 (                              IIIl111I                             ,                            Ill1II1l 												)												                            ,                            parent 															=															camera 												.												ui                              ,                             model 																=																lI1lIlIl 											)											




                                                            Text                       (                      I1II1II1 													,													position 											=																								(													II11lI1I 															,															IllIl111 											)																							,												scale 								=								                                (                                l1l1Il1l 											/											window                        .                       aspect_ratio                    ,                   l1l1Il1l 									)									                  ,                  origin 									=									                         (                         Ill1II1l 									,									ll1l11II 								)								                                ,                                parent                      =                     II1l1I11 											)											




                                                            PyneButton                    (                   text 												=												lIIIlI1l 											,											xPos 									=									l1I11l1l 																,																yPos                    =                   l111111I 											,											ySize 														=														l1I1lIll                        ,                       xSize                  =                 II1lI11I 																/																window                 .                aspect_ratio 													,													onClick                   =                  returntogame 												,												tooltip                    =                   I11I1I11 												,												parent                               =                              II1l1I11 																)																





                                                            I1Il11Il                            =                           Entity 												(												parent                     =                    II1l1I11 											,											position 															=																															(																lIl11III                         ,                        ll1l11II 												)																				)								





                                                            PyneButton 								(								text 																=																IIIlI1I1 															,															xPos                               =                                                            -                              llIIIIIl 										/										window 										.										aspect_ratio                                ,                               yPos 									=									l1l1I1ll 																,																ySize 														=														III1l1II 										,										xSize 								=								l1III11I 																/																window                             .                            aspect_ratio                              ,                             onClick 											=											save_world 								,								tooltip                                 =                                l1Il11lI 																,																parent 															=															I1Il11Il                                 )                                

                                                            PyneButton                        (                       text                      =                     I111l11I 															,															xPos 									=									llIIIIIl                      /                     window 											.											aspect_ratio                                ,                               yPos 												=												Ill1II1l 											,											ySize                     =                    l1I1lIll                             ,                            xSize                  =                 l1III11I                      /                     window 												.												aspect_ratio                    ,                   onClick                               =                              lambda 													:													l1Il1111 													,													tooltip 												=												I1I1ll11                             ,                            parent                     =                    I1Il11Il 										,										glitched                              =                             fuck_up 								(								l1llIIl1                          )                                                )                       






                                                            PyneButton                           (                          text 																=																IlIIIII1 									,									xPos                             =                            l1I11l1l                   ,                  yPos                  =                 								-								II1IIIlI                             ,                            ySize                               =                              III1l1II 														,														xSize                               =                              Ill1l1I1 										/										window                            .                           aspect_ratio                  ,                 onClick                               =                              PyneQuit 									,									tooltip 												=												lI1l111I 								,								parent 									=									II1l1I11                           )                          








                                                            II1l1I11                            .                           __stateText                     =                    Text 										(										IIlIIII1                           ,                          position 														=																													(															II11lI1I                           ,                                          -                IllIl111 												)												                ,                scale                      =                     															(															l11111ll 								/								window                          .                         aspect_ratio 										,										IlI11ll1                              )                                                           ,                              origin                               =                              																(																l1IIII1I 													,													lIl11III                             )                            									,									parent                   =                  II1l1I11                           )                          







                                                            II1l1I11                   .                  hideMenu                   (                                                 )                               








                                        def showMenu 								(								self                 )                                               :                               

                                                            IIIl11l1 									=									self 






                                                            IIIl11l1                          .                         visible 																=																fuck_up                        (                       lllI1111 										)										
                                                            for IllIllI1 in                           [                          I1lIIl1I                 ]                										:										







                                                                                if 													(													                          (                          lIlI1ll1 or not I1llll11 								(								lllII1ll 								)																					)													and 																(																IIIlIIlI 												<												llllll11 and l1II1llI 																!=																IIIl1l1l 										)																				)										and 															(															                           (                           l1ll1III                      !=                     l1llIIIl or I1llll11 									(									ll1II1ll                           )                          														)														or                        (                       not l1111l1l 										(										II1l1lII                              )                             or not Il11lIll 													.													llIl11II                       (                      llI1II11                                 )                                											)											                    )                                               :                           







                                                                                                    for IIIlIll1 in 										(										IlII1l11 								,								                              )                                                          :                            








                                                                                                                        for IIIIIIll in IIIl11l1                    .                   children 															:															








                                                                                                                                            ll11IllI 												=												lIIl1Ill 






                                                                                                                                            I11IIl11 									=									l11lIlII 

                                                                                                                                            if lIl1I11I 															(															IllIl11I 																,																llIIIll1 													)													                              :                              





                                                                                                                                                                I11IIl11 								=								l1llllI1 

                                                                                                                                            else                               :                              


                                                                                                                                                                I11IIl11 															=															IlIIlIll 

                                                                                                                                            if I11IIl11                             ==                            II1lllII 									:									

                                                                                                                                                                if not l1111l1l                                (                               l1II1II1                            )                                           :                



                                                                                                                                                                                    I11IIl11 														=														Il1llII1 






                                                                                                                                                                else 												:												






                                                                                                                                                                                    I11IIl11 															=															IIIlll11 






                                                                                                                                            if I11IIl11 																==																IllIl11I                      :                     

                                                                                                                                                                ll11IllI                       =                      Il111l1I 



                                                                                                                                            if I11IIl11 								==								l1lI1lI1 											:											




                                                                                                                                                                ll11IllI                    =                   lIlIlIll 

                                                                                                                                            if ll11IllI                               ==                              Il1llII1 															:															


                                                                                                                                                                IIl1I1l1                               =                              I1lI1lIl 



                                                                                                                                                                if lI11I1l1                              (                             IlIIIlIl                   ,                  ll1III1I                      )                                                  :                             




                                                                                                                                                                                    IIl1I1l1 											=											l1IllllI 






                                                                                                                                                                else 													:													





                                                                                                                                                                                    IIl1I1l1 											=											IllIll1l 
                                                                                                                                                                if IIl1I1l1                              ==                             lIIl1Ill 													:													




                                                                                                                                                                                    l1I11l11                         =                        IlI1ll1l 





                                                                                                                                                                                    II1IlIlI                      =                     IlIll1l1 




                                                                                                                                                                                    lIIlI1lI 												=												IlI111II 





                                                                                                                                                                                    if not I1IlII11                           :                          


                                                                                                                                                                                                        lIIlI1lI                           =                          II11IlIl 


                                                                                                                                                                                    else                               :                              





                                                                                                                                                                                                        lIIlI1lI 															=															IlI1II1l 



                                                                                                                                                                                    if lIIlI1lI 									==									IlI1II1l 																:																



                                                                                                                                                                                                        if not l1111l1l                       (                      l1IlI111 															)															                 :                 







                                                                                                                                                                                                                            lIIlI1lI 										=										lI11lIIl 

                                                                                                                                                                                                        else                         :                        









                                                                                                                                                                                                                            lIIlI1lI 																=																II11IlIl 
                                                                                                                                                                                    if lIIlI1lI                         ==                        IllIIII1 														:														
                                                                                                                                                                                                        II1IlIlI                                 =                                II1l1lI1 









                                                                                                                                                                                    if lIIlI1lI                   ==                  lllI1ll1                       :                      






                                                                                                                                                                                                        II1IlIlI                       =                      I1l1III1 






                                                                                                                                                                                    if II1IlIlI                   ==                  IlI1lllI                          :                         









                                                                                                                                                                                                        lI1l111l 												=												II11Illl 
                                                                                                                                                                                                        if not I1llll11                          (                         lIllIIlI 												)																								:												



                                                                                                                                                                                                                            lI1l111l 													=													III1llI1 








                                                                                                                                                                                                        else                               :                              







                                                                                                                                                                                                                            lI1l111l 												=												l11111II 

                                                                                                                                                                                                        if lI1l111l                       ==                      l1ll1III 									:									









                                                                                                                                                                                                                            if not l1111l1l                                (                               IllI11II                              )                             											:											







                                                                                                                                                                                                                                                lI1l111l 															=															l1I11II1 






                                                                                                                                                                                                                            else 													:													


                                                                                                                                                                                                                                                lI1l111l 																=																Il11l1II 





                                                                                                                                                                                                        if lI1l111l 										==										Il111lII 											:											





                                                                                                                                                                                                                            II1IlIlI                            =                           l1ll1llI 



                                                                                                                                                                                                        if lI1l111l 										==										I1IIlIIl 													:													







                                                                                                                                                                                                                            II1IlIlI                               =                              lIIlIl1l 






                                                                                                                                                                                    if II1IlIlI                  ==                 l1l1Il1l                         :                        





                                                                                                                                                                                                        l1I11l11                 =                lll11IIl 









                                                                                                                                                                                    if II1IlIlI 																==																llIlIIll 																:																









                                                                                                                                                                                                        l1I11l11                           =                          l1I1lII1 








                                                                                                                                                                                    if l1I11l11 															==															l1I1lII1                               :                              




                                                                                                                                                                                                        lI1lll1l                  =                 l1l1IlIl 
                                                                                                                                                                                                        lllI11lI                 =                I1lIl1ll 








                                                                                                                                                                                                        if not Il11lIll 												.												llIl11II                            (                           III1IllI                     )                    													:													




                                                                                                                                                                                                                            lllI11lI                  =                 lIl111II 



                                                                                                                                                                                                        else 												:												




                                                                                                                                                                                                                            lllI11lI 																=																IIII11ll 









                                                                                                                                                                                                        if lllI11lI 																==																l1lIIllI                    :                   

                                                                                                                                                                                                                            if lI11I1l1                                 (                                I1l11Ill 															,															l1I1lIlI                                 )                                                    :                    







                                                                                                                                                                                                                                                lllI11lI                 =                l11l1lII 





                                                                                                                                                                                                                            else                 :                








                                                                                                                                                                                                                                                lllI11lI                      =                     lIIIl11l 









                                                                                                                                                                                                        if lllI11lI                 ==                IlIl1II1                          :                         



                                                                                                                                                                                                                            lI1lll1l                                =                               IlI1II1l 








                                                                                                                                                                                                        if lllI11lI                            ==                           l11l1lII                     :                    


                                                                                                                                                                                                                            lI1lll1l                 =                II11IIlI 


                                                                                                                                                                                                        if lI1lll1l 									==									lll11IIl 												:												








                                                                                                                                                                                                                            lIIIllI1 															=															I1lIIl1I 


                                                                                                                                                                                                                            if not l1l1IlIl 															:															
                                                                                                                                                                                                                                                lIIIllI1                                =                               l1lIlI1l 





                                                                                                                                                                                                                            else                      :                     









                                                                                                                                                                                                                                                lIIIllI1                   =                  IIl1l11I 






                                                                                                                                                                                                                            if lIIIllI1 								==								II111I1I                  :                 






                                                                                                                                                                                                                                                if IIII11lI 														(														IIl1III1 															,															I111IIl1 													)													                :                




                                                                                                                                                                                                                                                                    lIIIllI1                        =                       lI1IlI11 









                                                                                                                                                                                                                                                else 															:															





                                                                                                                                                                                                                                                                    lIIIllI1                       =                      lIIl1lI1 




                                                                                                                                                                                                                            if lIIIllI1                     ==                    lIlI11I1                      :                     





                                                                                                                                                                                                                                                lI1lll1l                                 =                                l11111ll 




                                                                                                                                                                                                                            if lIIIllI1 										==										l1l1lIl1                     :                    






                                                                                                                                                                                                                                                lI1lll1l 								=								l1lI1II1 



                                                                                                                                                                                                        if lI1lll1l 									==									l1l1IIIl                               :                              









                                                                                                                                                                                                                            l1I11l11 											=											IlI1IIII 









                                                                                                                                                                                                        if lI1lll1l 												==												Illl11II 													:													





                                                                                                                                                                                                                            l1I11l11                             =                            IllIlIll 


                                                                                                                                                                                    if l1I11l11 								==								lll11IIl 													:													







                                                                                                                                                                                                        IIl1I1l1                      =                     Il1IllIl 








                                                                                                                                                                                    if l1I11l11                                 ==                                IllIlIll                    :                   

                                                                                                                                                                                                        IIl1I1l1                  =                 I1IllllI 








                                                                                                                                                                if IIl1I1l1                              ==                             lII1IlII                          :                         

                                                                                                                                                                                    ll11IllI 										=										lIIlIl1l 





                                                                                                                                                                if IIl1I1l1                   ==                  llI111ll 																:																







                                                                                                                                                                                    ll11IllI                 =                IlIIIlIl 
                                                                                                                                            if ll11IllI                      ==                     IlIIIlIl 																:																





                                                                                                                                                                pass 
                                                                                                                                            if ll11IllI 															==															lI11llll 								:								




                                                                                                                                                                l1Illl11 									=									Il11l1II 






                                                                                                                                                                l1l1lIll 									=									l1lIIllI 







                                                                                                                                                                if not Il11lIll                              .                             llIl11II 														(														lIl1IlIl                             )                            												:												








                                                                                                                                                                                    l1l1lIll 											=											III1llI1 





                                                                                                                                                                else 										:										





                                                                                                                                                                                    l1l1lIll                   =                  lI1l11lI 


                                                                                                                                                                if l1l1lIll                              ==                             l1l11Il1 										:										







                                                                                                                                                                                    if not I1llll11 									(									I1l1III1 													)													                         :                         








                                                                                                                                                                                                        l1l1lIll 																=																I1111IlI 


                                                                                                                                                                                    else                       :                      





                                                                                                                                                                                                        l1l1lIll                    =                   l11lI1l1 




                                                                                                                                                                if l1l1lIll                        ==                       lIII111l                     :                    



                                                                                                                                                                                    l1Illl11                          =                         I11lIIII 







                                                                                                                                                                if l1l1lIll 													==													I1lIIl1I                             :                            







                                                                                                                                                                                    l1Illl11 									=									l1lIlI1l 





                                                                                                                                                                if l1Illl11                          ==                         lIlIl111 											:											


                                                                                                                                                                                    lIIl1II1 															=															IlIlIll1 



                                                                                                                                                                                    if not l1111l1l 								(								llI1l11l 												)												                             :                             



                                                                                                                                                                                                        lIIl1II1 														=														lI1Il1ll 




                                                                                                                                                                                    else 								:								

                                                                                                                                                                                                        lIIl1II1 									=									l1I11IlI 


                                                                                                                                                                                    if lIIl1II1 								==								lllI1l1l 												:												









                                                                                                                                                                                                        if not IlIlI1II 								(								IIIIIIll 										,										Entity 												)												                       :                       


                                                                                                                                                                                                                            lIIl1II1 								=								II11Illl 





                                                                                                                                                                                                        else                      :                     





                                                                                                                                                                                                                            lIIl1II1 									=									lI1Il1ll 




                                                                                                                                                                                    if lIIl1II1 												==												l111lII1                                :                               









                                                                                                                                                                                                        l1Illl11 								=								I1111IlI 







                                                                                                                                                                                    if lIIl1II1                 ==                lll1111l                         :                        






                                                                                                                                                                                                        l1Illl11 										=										IlI11llI 


                                                                                                                                                                if l1Illl11 										==										lI1l11lI 											:											




                                                                                                                                                                                    pass 






                                                                                                                                                                if l1Illl11 													==													llIII1lI                     :                    






                                                                                                                                                                                    pass 


                                                                                                                                                                IIIIIIll                  .                 enabled 																=																fuck_up                      (                     IlIl11Il 													)													

                                        def hideMenu 											(											self                       )                      									:									




                                                            lIlIllIl 														=														self 
                                                            lIlIllIl 												.												visible                                =                               fuck_up                                (                               I1IlIIlI                      )                     

                                                            for lIllll1I in lIlIllIl                    .                   children                   :                  





                                                                                l1ll1IIl 														=														IIIlll11 


                                                                                l1I1III1 										=										l11l1lII 





                                                                                III11l1I                          =                         l1lIlI1l 





                                                                                lllll1lI                                =                               llIIIll1 







                                                                                I1lIIIIl 										=										IllIlIll 
                                                                                if not Il11lIll                      .                     llIl11II 													(													II1I1l1I                          )                         													:													


                                                                                                    I1lIIIIl 																=																lIl111II 


                                                                                else                         :                        








                                                                                                    I1lIIIIl 															=															lIl1I11l 





                                                                                if I1lIIIIl                             ==                            l1II1llI 												:												









                                                                                                    if not l1111l1l                                (                               l11I1I1I                 )                                              :                              







                                                                                                                        I1lIIIIl                            =                           I1l1lIll 






                                                                                                    else 													:													





                                                                                                                        I1lIIIIl                            =                           IlI11ll1 





                                                                                if I1lIIIIl                  ==                 lIl111II 													:													

                                                                                                    lllll1lI 													=													IIllIl11 


                                                                                if I1lIIIIl                                ==                               IIll11I1                             :                            







                                                                                                    lllll1lI                                 =                                IIII1IIl 








                                                                                if lllll1lI                       ==                      IIII1IIl 								:								







                                                                                                    I11lIllI 								=								IIll11I1 



                                                                                                    if not IIII11lI 								(								lllI1ll1 								,								I1lIIl1I 															)															                            :                            



                                                                                                                        I11lIllI                           =                          l1I11II1 






                                                                                                    else                            :                           







                                                                                                                        I11lIllI 													=													lIIl11II 








                                                                                                    if I11lIllI                   ==                  l1l1l11I 										:										
                                                                                                                        if not Il11lIll 									.									llIl11II 									(									I1IIlIIl                          )                                             :                    




                                                                                                                                            I11lIllI                             =                            IlIIl1I1 







                                                                                                                        else                             :                            





                                                                                                                                            I11lIllI                  =                 l1IllI1I 





                                                                                                    if I11lIllI 																==																Il1lIl1l                     :                    

                                                                                                                        lllll1lI 														=														I1IlIIII 








                                                                                                    if I11lIllI                        ==                       l11l1I11                            :                           
                                                                                                                        lllll1lI 													=													l1l1II1I 





                                                                                if lllll1lI                               ==                              IIllIl11 																:																



                                                                                                    III11l1I 								=								l11l11l1 


                                                                                if lllll1lI 								==								lIII111l 															:															


                                                                                                    III11l1I                          =                         I111l111 


                                                                                if III11l1I                      ==                     IlIIIlIl 														:														
                                                                                                    IlII1l1I 												=												IIl1l111 


                                                                                                    l1IllIll 													=													IIIlI1lI 









                                                                                                    if not llIllIlI                          :                         



                                                                                                                        l1IllIll                          =                         Il111IIl 


                                                                                                    else 																:																






                                                                                                                        l1IllIll                                 =                                lIIl1Ill 


                                                                                                    if l1IllIll 											==											I1llllIl 											:											








                                                                                                                        if not lIl1I11I 														(														l1I11lIl 											,											l1l1ll1I                         )                                                        :                                









                                                                                                                                            l1IllIll 														=														lll1l1ll 



                                                                                                                        else 								:								




                                                                                                                                            l1IllIll 															=															lI1l11lI 




                                                                                                    if l1IllIll 																==																lll1Il1I                             :                            





                                                                                                                        IlII1l1I                               =                              IIllIlI1 







                                                                                                    if l1IllIll 																==																l1IllllI                       :                      







                                                                                                                        IlII1l1I 																=																IllIIllI 


                                                                                                    if IlII1l1I 											==											IIlIIl1l 														:														
                                                                                                                        l1IlIll1 										=										l111I11l 

                                                                                                                        if not IIlI1I11 													:													



                                                                                                                                            l1IlIll1                  =                 IIIlll11 

                                                                                                                        else 														:														


                                                                                                                                            l1IlIll1                         =                        Il111l1I 





                                                                                                                        if l1IlIll1 														==														IlIIIlIl                      :                     



                                                                                                                                            if not Il11lIll 										.										llIl11II                                 (                                III1IlII 															)															                           :                           


                                                                                                                                                                l1IlIll1                   =                  II1l1lI1 



                                                                                                                                            else 									:									




                                                                                                                                                                l1IlIll1 															=															IIIlll11 




                                                                                                                        if l1IlIll1 								==								IlIIlIll 													:													




                                                                                                                                            IlII1l1I 									=									lI1IlI11 
                                                                                                                        if l1IlIll1 																==																lI11llll                               :                              






                                                                                                                                            IlII1l1I                     =                    l1IlI111 





                                                                                                    if IlII1l1I                          ==                         I1l1II1l 																:																


                                                                                                                        III11l1I 										=										II11Illl 



                                                                                                    if IlII1l1I                   ==                  II1l11Il 														:														


                                                                                                                        III11l1I                           =                          l11IlI1I 








                                                                                if III11l1I                                ==                               l1lIIllI                             :                            






                                                                                                    l1I1III1                     =                    l1llllI1 

                                                                                if III11l1I 															==															II11Illl                         :                        








                                                                                                    l1I1III1                      =                     lIl1I11l 

                                                                                if l1I1III1 													==													l11111Il 															:															




                                                                                                    if not Il11lIll 													.													llIl11II                                (                               IllI1IIl 															)																								:									







                                                                                                                        l1I1III1 																=																lIl1IIIl 









                                                                                                    else 												:												




                                                                                                                        l1I1III1 											=											Illl1II1 


                                                                                if l1I1III1                       ==                      III1IlII                              :                             







                                                                                                    l1ll1IIl 															=															IlI11ll1 



                                                                                if l1I1III1                              ==                             I1IllllI 								:								






                                                                                                    l1ll1IIl 										=										Il1lIl1l 






                                                                                if l1ll1IIl 											==											Il1lIl1l 													:													








                                                                                                    llIIII1l                        =                       IllIIII1 








                                                                                                    if not IlIIII1l                             (                            IlII11Il 										,										I1l1llII 														)														                        :                        




                                                                                                                        llIIII1l                     =                    IllIlI1l 




                                                                                                    else 															:															
                                                                                                                        llIIII1l 												=												IIII11ll 



                                                                                                    if llIIII1l                      ==                     II1IlII1                   :                  





                                                                                                                        if not llllIIII                         (                        llI11llI                  ,                 l1llll1I 														)																								:										





                                                                                                                                            llIIII1l                            =                           lIIl1lI1 







                                                                                                                        else 															:															

                                                                                                                                            llIIII1l                      =                     l11IlI1I 

                                                                                                    if llIIII1l 																==																l1lIIllI                  :                 




                                                                                                                        l1ll1IIl 														=														IIll11I1 








                                                                                                    if llIIII1l 													==													l1l1lIl1 												:												






                                                                                                                        l1ll1IIl 														=														llll1IlI 





                                                                                if l1ll1IIl 										==										II11IIlI 																:																



                                                                                                    pass 


                                                                                if l1ll1IIl                  ==                 llll1IlI                         :                        




                                                                                                    lI1111II                      =                     l1IIIll1 








                                                                                                    IIIl1lll                            =                           Il1IllIl 




                                                                                                    if not IlIIII1l                   (                  Illll1I1                       ,                      I1IlII11                  )                                       :                      







                                                                                                                        IIIl1lll 									=									llI1lIII 

                                                                                                    else                      :                     

                                                                                                                        IIIl1lll 																=																IIl1I1Il 






                                                                                                    if IIIl1lll 																==																llI1lIII                  :                 









                                                                                                                        if not IlIlI1II 												(												lIllll1I                        ,                       Entity                          )                                                       :                              









                                                                                                                                            IIIl1lll 								=								II1llllI 









                                                                                                                        else 												:												



                                                                                                                                            IIIl1lll                          =                         lIllIIll 








                                                                                                    if IIIl1lll 										==										I1llI11I                   :                  








                                                                                                                        lI1111II                                 =                                lIllllII 








                                                                                                    if IIIl1lll                               ==                              IIl1I1Il 													:													
                                                                                                                        lI1111II                             =                            lIlI1II1 



                                                                                                    if lI1111II                            ==                           IlI1ll1l                    :                   







                                                                                                                        l1II11ll                    =                   l1IllI1l 
                                                                                                                        if not l11l1lII 										:										

                                                                                                                                            l1II11ll                           =                          Ill1IIIl 





                                                                                                                        else 																:																









                                                                                                                                            l1II11ll 								=								Il111l1I 






                                                                                                                        if l1II11ll                                ==                               l11I1I1l 															:															




                                                                                                                                            if not l1ll1III 											:											

                                                                                                                                                                l1II11ll 									=									l11l11l1 
                                                                                                                                            else                     :                    




                                                                                                                                                                l1II11ll                               =                              I1lllIl1 




                                                                                                                        if l1II11ll                 ==                Ill1I11I                      :                     

                                                                                                                                            lI1111II 														=														l11lI1l1 






                                                                                                                        if l1II11ll 												==												l1l1IlIl 											:											








                                                                                                                                            lI1111II 														=														Il111l1I 

                                                                                                    if lI1111II 											==											l1l1IlIl 								:								





                                                                                                                        pass 


                                                                                                    if lI1111II 												==												lllI1ll1                             :                            


                                                                                                                        pass 









                                                                                                    lIllll1I 								.								enabled 									=									fuck_up                              (                             II1Ill11 																)																


                                        def showStateText 											(											self 															,															text                              :                             str 													)																												:															

                                                            (                            l11I11II 													,													IIIII1ll                            )                                                    =                                          (                 self                           ,                          text                    )                   


                                                            l11I11II 																.																__stateText 										.										text                          =                         IIIII1ll 

                                                            invoke 								(								l11I11II 									.									__stateText                   .                  __setattr__                        ,                       IllI1ll1 											,											lIIlllIl                             ,                            delay                                 =                                lI11llll                  )                 

                    global escmenu 



                    escmenu                     =                    EscMenu                  (                 															)															







                    class Sky 																(																Entity 									)																			:										








                                        def __init__ 														(														self 												)												                    :                    





                                                            l1I1I1l1 													=													self 
                                                            super 								(								                       )                       																.																__init__                   (                  parent 											=											scene 														,														model 											=											llIIlIl1                  ,                 texture                                =                               I1ll1IIl                              ,                             scale 													=													IIlIIlI1                       ,                      double_sided 										=										fuck_up                     (                    IlIllll1                     )                    															)															


                                        def update                        (                       self 												)												                               :                               







                                                            l111I1II 												=												self 







                                                            l111I1II                         .                        position 										=										player                             .                            position 
                    l11Il1II 

                    load_world 															(															                         )                         







                    global move_entity 





                    def move_entity                      (                     e1                             =                            ra 									,									e2 								=								player 													,													speed                          =                         llIIIIII 									,									gravity 										=										                   -                   l1l111ll                  ,                 y_velocity 													=													II11lI1I 														,														power 								=								IIll11I1 										,										isdamaging                                 =                                fuck_up                         (                        IlIl11Il                   )                  												,												knowback                          =                         fuck_up 									(									II1III11 																)																                     ,                     collisions 									=									fuck_up 													(													IlIllll1 									)									                 )                                        :                       






                                        (									IIlIlIII 															,															Il1IIl1l                       ,                      llIlllII 															,															Il1111lI                       ,                      IIlII1ll 								,								l1I1Illl 										,										lIlI11l1 										,										IlIlll1I                   ,                  Il1ll1Il 								)								                               =                               									(									power 													,													isdamaging 																,																e2                 ,                collisions 											,											gravity                  ,                 knowback 																,																speed                         ,                        e1 																,																y_velocity                    )                   
                                        l1ll111I                 =                l1lIIllI 

                                        II11l11l 													=													Il11I111 
                                        if lI11I1l1                      (                     lI1llI11 								,								IllIIllI 										)																									:															









                                                            II11l11l                             =                            lIIlIl1l 
                                        else                                 :                                



                                                            II11l11l 															=															II1lIIll 
                                        if II11l11l 															==															IllI1l11                       :                      
                                                            if not Il11lIll 								.								llIl11II                              (                             l1I11II1                               )                              								:								





                                                                                II11l11l                             =                            l1l1Il1l 




                                                            else 															:															




                                                                                II11l11l 													=													lll11IIl 




                                        if II11l11l 												==												lll11IIl 															:															




                                                            l1ll111I 													=													IlllIIl1 




                                        if II11l11l                   ==                  l1l1Il1l 																:																








                                                            l1ll111I                 =                lII11l1I 






                                        if l1ll111I 																==																IlllIIl1 											:											



                                                            l1I1IlIl                            =                           IlIl1II1 

                                                            if not l1111l1l 								(								l1IIIll1 									)									                      :                      








                                                                                l1I1IlIl                           =                          l1l11Il1 


                                                            else 														:														




                                                                                l1I1IlIl                    =                   l11l11l1 





                                                            if l1I1IlIl                       ==                      ll11IlIl                   :                  

                                                                                if IIII11lI                        (                       player 										.										enabled                            ,                           fuck_up 																(																l1llIIl1                              )                                                  )                                     :                

                                                                                                    l1I1IlIl                                =                               lIll1I1l 

                                                                                else                           :                          
                                                                                                    l1I1IlIl                   =                  l1l11Il1 









                                                            if l1I1IlIl                             ==                            llI11llI                     :                    






                                                                                l1ll111I 												=												l111l1lI 






                                                            if l1I1IlIl                          ==                         Il11l1II                       :                      





                                                                                l1ll111I                    =                   II1l1Il1 







                                        if l1ll111I                  ==                 lII11l1I 										:										








                                                            pass 




                                        if l1ll111I                               ==                              IIIlll11                         :                        





                                                            Il1IlI1l                       =                      												(												llIlllII                            .                           position 																-																IlIlll1I 														.														position 															)															                          .                          normalized 															(																												)													







                                                            I1llIIll 										=																					(											llIlllII 											.											position 													-													IlIlll1I 														.														position                     )                    										.										length                                 (                                												)												

                                                            IlIlll1I                           .                          rotation_y 													=													atan2                          (                         Il1IlI1l                       .                      x 															,															Il1IlI1l 														.														z 																)																										*										Il1lll1I 								/								pi 
                                                            lllIII11                  =                 IIllIlI1 
                                                            llI1llll 											=											llII1llI 

                                                            if not Il11lIll 											.											llIl11II 								(								III1IllI                          )                         													:													









                                                                                llI1llll                   =                  l1II1II1 
                                                            else 											:											







                                                                                llI1llll                                 =                                IllllII1 








                                                            if llI1llll 											==											IllllII1 								:								








                                                                                if not l1IIl1ll                         :                        





                                                                                                    llI1llll                  =                 lIlI1ll1 




                                                                                else                             :                            
                                                                                                    llI1llll 																=																l1lI1II1 



                                                            if llI1llll 										==										IllIlIll 																:																









                                                                                lllIII11                         =                        lll1l1ll 



                                                            if llI1llll                             ==                            lIllllll                          :                         

                                                                                lllIII11                       =                      IIIIIlI1 


                                                            if lllIII11                          ==                         l1IIl1ll 										:										



                                                                                l1lll1lI                                =                               IIIl1111 



                                                                                if not Il11lIll                   .                  llIl11II                  (                 llIlIII1 										)																			:									




                                                                                                    l1lll1lI 											=											l111lII1 






                                                                                else                        :                       
                                                                                                    l1lll1lI 														=														l1ll1Il1 





                                                                                if l1lll1lI                   ==                  llll1IlI                    :                   


                                                                                                    if IlIIII1l 																(																I1llIIll                   ,                  II11IIlI                          )                                           :                  


                                                                                                                        l1lll1lI                          =                         IlI1ll1l 







                                                                                                    else                            :                           


                                                                                                                        l1lll1lI 									=									IIl1l11I 








                                                                                if l1lll1lI 										==										lIIl1lI1 														:														








                                                                                                    lllIII11 															=															I111lIII 

                                                                                if l1lll1lI                 ==                lIlIl111 											:											





                                                                                                    lllIII11 												=												llI1II11 




                                                            if lllIII11                       ==                      lll1l1ll 												:												






                                                                                pass 





                                                            if lllIII11 															==															l11111Il 										:										




                                                                                IlIlll1I 											.											position                                 +=                                Il1IlI1l 											+											Vec3                     (                    ll1l11II                      ,                     IIlII1ll 										,										Ill1II1l 													)													                         *                         lIlI11l1 										*										time 															.															dt 


                                                            l1Illl1l                    =                   lIIl1Ill 


                                                            l11l1Ill 										=										I11lI11l 

                                                            if not Il11lIll 													.													llIl11II 													(													lI1ll11I 											)																								:													



                                                                                l11l1Ill 									=									l1l1ll1l 


                                                            else                        :                       


                                                                                l11l1Ill                              =                             lIlI1II1 






                                                            if l11l1Ill                       ==                      lIlI1II1                            :                           



                                                                                if not Il11lIll 										.										llIl11II                   (                  IllIll1l 								)								                :                

                                                                                                    l11l1Ill 												=												IlIIII1I 







                                                                                else 									:									


                                                                                                    l11l1Ill 																=																l1l1lllI 


                                                            if l11l1Ill 								==								I1l11Ill 										:										




                                                                                l1Illl1l                       =                      I1I11IIl 





                                                            if l11l1Ill                                ==                               IllIIII1 													:													

                                                                                l1Illl1l                  =                 l1l1IIIl 









                                                            if l1Illl1l                             ==                            II11IIlI 															:															







                                                                                Il1lIlIl 									=									Il111lII 


                                                                                if llllIIII                            (                           I1llIIll 																,																l1l1IIIl 														)																													:															






                                                                                                    Il1lIlIl                                 =                                Illl1II1 


                                                                                else 															:															
                                                                                                    Il1lIlIl                              =                             IlI11llI 
                                                                                if Il1lIlIl 															==															l111l1lI 															:															





                                                                                                    if not II1IIIll                            :                           
                                                                                                                        Il1lIlIl 											=											l111I11l 





                                                                                                    else                   :                  







                                                                                                                        Il1lIlIl 									=									llI1l1II 


                                                                                if Il1lIlIl 											==											IlI11llI                   :                  
                                                                                                    l1Illl1l                             =                            l1IIIll1 






                                                                                if Il1lIlIl                           ==                          Il1l1IlI                                :                               








                                                                                                    l1Illl1l 														=														IIlllIll 








                                                            if l1Illl1l 								==								Il111IIl 													:													









                                                                                pass 

                                                            if l1Illl1l 									==									IlllI1lI                 :                
                                                                                I1l1lI1l                  =                 lll1I1II 

                                                                                l1IlIl11 														=														llIlIIIl 



                                                                                if not I1llll11 													(													llIIIIlI                           )                          														:														









                                                                                                    l1IlIl11                                =                               IIIll1Il 





                                                                                else 								:								



                                                                                                    l1IlIl11 								=								IIllIl11 



                                                                                if l1IlIl11                      ==                     IIIll1Il                           :                          





                                                                                                    if not I1llll11 												(												I1lllIl1 											)																								:													









                                                                                                                        l1IlIl11                        =                       IIllIl11 



                                                                                                    else 										:										







                                                                                                                        l1IlIl11 											=											Il11l1II 







                                                                                if l1IlIl11 										==										IIIIIlII 														:														









                                                                                                    I1l1lI1l 									=									l1II1ll1 






                                                                                if l1IlIl11 													==													Il11l1II                             :                            









                                                                                                    I1l1lI1l 														=														lIIl11II 


                                                                                if I1l1lI1l                  ==                 l111l1lI 											:											



                                                                                                    l11l11Il 															=															Il1l1IIl 









                                                                                                    if not IIII11lI                  (                 Il1IIl1l 									,									fuck_up                   (                  l1IIlII1 												)												                                )                                														:														




                                                                                                                        l11l11Il                                =                               l11IlI1I 








                                                                                                    else 										:										


                                                                                                                        l11l11Il                  =                 lIll1Ill 






                                                                                                    if l11l11Il 								==								I111l111 													:													

                                                                                                                        if not IlI11llI 																:																

                                                                                                                                            l11l11Il 										=										lIll1Ill 



                                                                                                                        else 									:									









                                                                                                                                            l11l11Il                              =                             IIl1Il1l 



                                                                                                    if l11l11Il 														==														II1l11Il                            :                           





                                                                                                                        I1l1lI1l                               =                              IllIIII1 









                                                                                                    if l11l11Il                    ==                   lIllllll 											:											
                                                                                                                        I1l1lI1l                        =                       IlIIl1I1 






                                                                                if I1l1lI1l 																==																l1llIll1                          :                         







                                                                                                    pass 







                                                                                if I1l1lI1l 															==															lIIl11II                               :                              








                                                                                                    player 															.															damage 									(									IIlIlIII 																)																





                                                                                                    lII11Il1                           =                          lIl1lII1 







                                                                                                    Il1lIIIl 														=														llI1lIII 




                                                                                                    if not lIl1I11I                     (                    I11ll1I1 																,																IIl11II1 										)																									:															







                                                                                                                        Il1lIIIl                       =                      lI11ll1I 








                                                                                                    else                            :                           




                                                                                                                        Il1lIIIl 														=														l11lI1lI 









                                                                                                    if Il1lIIIl                     ==                    l1lll1II                         :                        







                                                                                                                        if not I1llll11 								(								IllIIllI 																)																													:													

                                                                                                                                            Il1lIIIl                    =                   IIIIIlI1 


                                                                                                                        else                       :                      


                                                                                                                                            Il1lIIIl                            =                           ll11III1 









                                                                                                    if Il1lIIIl                  ==                 l1IIl1ll                                :                               









                                                                                                                        lII11Il1 														=														ll1l1I11 



                                                                                                    if Il1lIIIl 															==															ll11III1 								:								





                                                                                                                        lII11Il1 									=									Ill111l1 
                                                                                                    if lII11Il1                  ==                 llII1llI 																:																








                                                                                                                        l1IlIl1l 												=												l111I1I1 






                                                                                                                        if not IIII11lI 													(													l1I1Illl                         ,                        fuck_up                      (                     lllI1111                         )                                                      )                              																:																





                                                                                                                                            l1IlIl1l                           =                          l1l1ll1l 




                                                                                                                        else 											:											
                                                                                                                                            l1IlIl1l                            =                           lIllllll 





                                                                                                                        if l1IlIl1l 									==									lIIll1II 									:									




                                                                                                                                            if not Illl1I11 										:										







                                                                                                                                                                l1IlIl1l                                =                               II11IllI 


                                                                                                                                            else                       :                      





                                                                                                                                                                l1IlIl1l                        =                       l11lIlII 









                                                                                                                        if l1IlIl1l                   ==                  l11lIlII 													:													








                                                                                                                                            lII11Il1 											=											Illl1II1 




                                                                                                                        if l1IlIl1l                   ==                  IIlIl11l 																:																









                                                                                                                                            lII11Il1                 =                IllI1l11 

                                                                                                    if lII11Il1 												==												I1lIl1ll                     :                    



                                                                                                                        IlIlll1I 										.										position 														=														IlIlll1I                    .                   position                               +                              Vec3 													(													l1l1IIIl                          ,                         l1II1lI1                        ,                       I11IIIll 											)											

                                                                                                    if lII11Il1 																==																lII11l1I 											:											


                                                                                                                        pass 







                                                            Ill11111                             =                            I1I11IIl 







                                                            IllI1I11                          =                         ll1III1I 



                                                            if not Il11lIll 																.																llIl11II                          (                         l1llIIll                   )                                    :                  








                                                                                IllI1I11                   =                  l1llIl1I 

                                                            else                      :                     



                                                                                IllI1I11                             =                            l1I11IlI 







                                                            if IllI1I11 								==								l1I11IlI 													:													





                                                                                if IlIIII1l 																(																llI1IlIl 															,															llIIIll1                          )                         															:															
                                                                                                    IllI1I11                           =                          lI11llll 






                                                                                else                            :                           


                                                                                                    IllI1I11                        =                       ll11lllI 





                                                            if IllI1I11                          ==                         Il1l1IIl 															:															






                                                                                Ill11111                     =                    I1l1I1lI 


                                                            if IllI1I11 														==														I1IlIIll 																:																




                                                                                Ill11111                          =                         l1l1II1I 
                                                            if Ill11111 								==								IIlIIll1 													:													









                                                                                ll1IIlll                     =                    Il11lI1l 





                                                                                if IIII11lI                                (                               Il1111lI 								,								fuck_up                       (                      IlIl11Il                          )                         															)															                             :                             





                                                                                                    ll1IIlll 								=								l1I1I1Il 



                                                                                else                                :                               






                                                                                                    ll1IIlll                     =                    Il11llll 
                                                                                if ll1IIlll                        ==                       I1llllIl                            :                           







                                                                                                    if not Il11lIll                         .                        llIl11II                   (                  II11Il1I                        )                                       :                





                                                                                                                        ll1IIlll                            =                           I1lIl1ll 





                                                                                                    else                      :                     



                                                                                                                        ll1IIlll                             =                            l11IlI1I 



                                                                                if ll1IIlll 														==														IIII11ll 										:										






                                                                                                    Ill11111                       =                      Il11lI1l 
                                                                                if ll1IIlll 												==												Il11llll 															:															



                                                                                                    Ill11111 															=															lll11IIl 





                                                            if Ill11111 												==												IlI1IIII 												:												
                                                                                IlIIIlll 										=										IlIlll1I                   .                  intersects 																(																												)												



                                                                                lIl1IlII                            =                           I1IllllI 
                                                                                l11IIl1I                              =                             I1l11lll 




                                                                                if not ll1I11II                            (                           IIIlll11 														,														l1lI11Il 													)																												:															



                                                                                                    l11IIl1I                 =                I11Il111 




                                                                                else                            :                           


                                                                                                    l11IIl1I                      =                     Il11l1II 




                                                                                if l11IIl1I                       ==                      IIIIIlI1 										:										



                                                                                                    if not IlIIIlll 														.														hit 											:											








                                                                                                                        l11IIl1I 								=								Il111lII 



                                                                                                    else 											:											


                                                                                                                        l11IIl1I 														=														IIIll1Il 


                                                                                if l11IIl1I                           ==                          l111I11l                               :                              


                                                                                                    lIl1IlII                   =                  I1I1llI1 





                                                                                if l11IIl1I 													==													III1llI1 													:													







                                                                                                    lIl1IlII                               =                              Illl1II1 









                                                                                if lIl1IlII                          ==                         lIlIl1ll                                :                               

                                                                                                    lII11I1I 																=																IIlIlIlI 






                                                                                                    if not l1l11Il1                           :                          





                                                                                                                        lII11I1I                          =                         I1llllIl 


                                                                                                    else 										:										


                                                                                                                        lII11I1I                       =                      lllI1ll1 


                                                                                                    if lII11I1I                        ==                       l11lI1l1 															:															







                                                                                                                        if not I1llll11                              (                             IllIlIll                            )                           																:																

                                                                                                                                            lII11I1I                    =                   l1IIllI1 









                                                                                                                        else 												:												






                                                                                                                                            lII11I1I                       =                      Il111IIl 




                                                                                                    if lII11I1I 																==																l1IllI1I 									:									







                                                                                                                        lIl1IlII                               =                              lII11l1I 







                                                                                                    if lII11I1I 																==																Il111IIl                          :                         

                                                                                                                        lIl1IlII 													=													Il1l1IlI 




                                                                                if lIl1IlII 															==															llI1l1II 											:											
                                                                                                    IlIlll1I 								.								position 															=															IlIlll1I                          .                         position 													+													Vec3 								(								Ill1II1l                   ,                  III1lllI                  ,                 l1IIII1I 														)														
                                                                                if lIl1IlII                   ==                  I1l1ll1I                      :                     




                                                                                                    pass 

                                                            if Ill11111                           ==                          Il11lI1l                  :                 








                                                                                pass 



                    camera                         .                        position                                 =                                player                                .                               position 






                    camera 													.													rotation                          =                         player 												.												rotation 






                    llI1llI1 								=								Sky 												(												                             )                             









def III1Illl 										(										I1IIIl1I 								)								                 :                 








                    global bossEnabled 









                    ll11l1ll 											=											IIl11I1I 


                    I1I111ll 													=													I1l1lIll 







                    if not I1I1l11l 													:													



                                        I1I111ll 												=												II1llllI 



                    else                           :                          

                                        I1I111ll                      =                     II1l11Il 


                    if I1I111ll                       ==                      lIll1Ill 								:								






                                        IIIll1ll 											=											II1I111I 
                                        if IIII11lI                        (                       player 																.																health 								,								Ill1II1l                               )                              											:											









                                                            IIIll1ll                                 =                                I1IlII11 



                                        else                       :                      

                                                            IIIll1ll 											=											l1l111l1 


                                        if IIIll1ll                             ==                            lIl1I1ll                 :                







                                                            if IIII11lI 								(								isplayerkilled                    ,                   fuck_up                      (                     I1IlIIlI                             )                            																)																                   :                   








                                                                                IIIll1ll 												=												I1IlII11 




                                                            else                               :                              



                                                                                IIIll1ll 									=									IllI1IIl 


                                        if IIIll1ll                                ==                               IllI1IIl 								:								








                                                            I1I111ll 										=										Il1llI11 







                                        if IIIll1ll                               ==                              IIl11II1                      :                     
                                                            I1I111ll                         =                        lll1IIll 


                    if I1I111ll                        ==                       lll1IIll                           :                          
                                        ll11l1ll 															=															IIllIl11 


                    if I1I111ll 																==																Ill1IIIl                  :                 





                                        ll11l1ll 								=								Il1llII1 







                    if ll11l1ll                        ==                       IIlIIll1                          :                         





                                        ll1Il11l                                 =                                lIlIl1ll 








                                        if not I1llll11                                 (                                Il111IlI                                 )                                										:										







                                                            ll1Il11l                    =                   ll11I1Il 
                                        else 									:									


                                                            ll1Il11l 												=												ll1Ill11 




                                        if ll1Il11l                         ==                        l1IllI1l 								:								








                                                            if not l1111l1l                           (                          lll1I1II 														)																												:														
                                                                                ll1Il11l                 =                IlI1I1I1 








                                                            else 																:																




                                                                                ll1Il11l 														=														lIll1I1l 


                                        if ll1Il11l                     ==                    I1lI1lIl                 :                
                                                            ll11l1ll 										=										ll1III1I 






                                        if ll1Il11l 										==										IIl11I1I 														:														








                                                            ll11l1ll                             =                            IllIl11I 







                    if ll11l1ll                          ==                         Il1llII1 									:									


                                        kill 								(								                 )                 

                    if ll11l1ll                              ==                             I11ll1I1                             :                            



                                        pass 

                    destroy 								(								player                   .                  cursor 										)										



                    player 															.															cursor 										=										Entity 														(														                              )                              




                    I11l1IIl                         =                        IlIIII1I 




                    l11Ill11                        =                       IlI11ll1 







                    if IlIIII1l 															(															I111II1I 														,														I1IlIIII                           )                                           :                 







                                        l11Ill11                         =                        IIlIIl1l 





                    else                               :                              









                                        l11Ill11 										=										IlIIII1I 








                    if l11Ill11                      ==                     IllIIllI 												:												




                                        if not lll1111l                        :                       









                                                            l11Ill11 									=									IIlIl11l 
                                        else                            :                           
                                                            l11Ill11 										=										llI1Il1l 






                    if l11Ill11                            ==                           II1IIIll 																:																
                                        I11l1IIl                       =                      I1I1l11l 






                    if l11Ill11 													==													l1l1ll1l                                 :                                


                                        I11l1IIl 												=												lIlIl1ll 




                    if I11l1IIl 																==																I1lIl1ll 															:															








                                        Il1lIlII 								=								l1ll1llI 

                                        if not l1111l1l 								(								IlI1I1I1 															)																										:											

                                                            Il1lIlII 												=												l111l1lI 









                                        else 									:									




                                                            Il1lIlII                              =                             IIIlll11 





                                        if Il1lIlII                      ==                     ll11Ill1                               :                              


                                                            III111ll 														=														l1111llI 
                                                            if llllIIII 											(											random                 .                random                        (                                          )                                        ,                     IIlIIlll                     )                                         :                     








                                                                                III111ll                                =                               llIIlI1I 


                                                            else                          :                         







                                                                                III111ll 														=														ll1l1I11 
                                                            if III111ll 											==											II1lIIll 																:																


                                                                                if not bossEnabled 														:														




                                                                                                    III111ll 										=										II1I11ll 
                                                                                else 									:									








                                                                                                    III111ll                       =                      IIIlIIlI 

                                                            if III111ll                          ==                         lI1Il1ll                         :                        





                                                                                Il1lIlII 																=																Il1lIlI1 

                                                            if III111ll 														==														ll1I1ll1                              :                             
                                                                                Il1lIlII 														=														Illl1II1 









                                        if Il1lIlII 										==										III1IlII                         :                        



                                                            I11l1IIl                           =                          Il1I111I 

                                        if Il1lIlII 								==								Il1lIlI1                           :                          

                                                            I11l1IIl                       =                      II1llllI 



                    if I11l1IIl                             ==                            lIlIl1ll 									:									





                                        boss1_sound                        .                       play 									(																				)											





                                        bossEnabled 											=											l1IIlII1 






                                        os 								.								startfile                             (                            os 															.															path 														.														join                    (                   os                        .                       path                               .                              dirname                             (                            os                         .                        path 								.								realpath 															(															__file__ 												)												                )                													,													II11ll1l 													)																											)														







                    if I11l1IIl 														==														Il1lIlI1 														:														








                                        pass 








                    I1lIII1I                   =                  Il11l1II 
                    IlIII1ll 								=								I1l1ll1I 
                    if not ll1I11II 													(													IlIIl1ll                     ,                    l11l11l1 												)												                           :                           





                                        IlIII1ll                                 =                                l11lI1l1 






                    else                  :                 







                                        IlIII1ll                 =                llIllIlI 
                    if IlIII1ll 								==								IlI1I1I1                           :                          








                                        if not lIllllll                             :                            









                                                            IlIII1ll 									=									lIllllII 









                                        else 											:											







                                                            IlIII1ll                    =                   II1IIlll 







                    if IlIII1ll                                 ==                                lIlIl1ll 									:									









                                        I1lIII1I 												=												I111II1I 


                    if IlIII1ll                             ==                            I1lIIl1I 												:												





                                        I1lIII1I 									=									l1I1lII1 



                    if I1lIII1I                               ==                              IIlIl11l 											:											




                                        Ill11I1l                    =                   l11l1lII 









                                        if not bossEnabled 										:										







                                                            Ill11I1l                        =                       I1llllIl 


                                        else                          :                         







                                                            Ill11I1l                      =                     lIlI1II1 


                                        if Ill11I1l                       ==                      IIlllIll                                :                               









                                                            if not lIl1I11I                               (                              IIIlll11 												,												IIIlll11                               )                                                   :                     








                                                                                Ill11I1l 													=													IlI1ll1l 


                                                            else 								:								
                                                                                Ill11I1l 													=													IlIl1II1 
                                        if Ill11I1l                          ==                         IIlllll1                        :                       









                                                            I1lIII1I 										=										lllI1l1l 









                                        if Ill11I1l 														==														llll11II 														:														



                                                            I1lIII1I                  =                 IlI1lllI 


                    if I1lIII1I 											==											l1I11II1                           :                          




                                        pass 









                    if I1lIII1I 													==													l1I11IlI 															:															





                                        move_entity                    (                   ra                                ,                               player                               ,                              llIIIIII                   ,                  												-												II1IIIlI 													,													II11lI1I 											,											IIll11I1 										,										lllI1111                              ,                             III1IIl1                      ,                     II1Ill11 														)														
                                        move_entity                            (                           mra 													,													player 										,										llIIIIII                        ,                       													-													lIl1I1l1                   ,                  Ill1II1l                             ,                            IIll11I1 											,											l1IIlII1 														,														III1IIl1 											,											I1IlIIlI 										)										








                                        IIIlI1l1                        =                       lIIl11II 





                                        III1I111 									=									I1l1I111 
                                        if not Il11lIll 									.									llIl11II 								(								l1llIll1 											)																							:												







                                                            III1I111 												=												lII1IlII 

                                        else 														:														









                                                            III1I111                                 =                                lIlI11I1 








                                        if III1I111 														==														I1l1II1l                      :                     



                                                            if not Il11lIll                       .                      llIl11II                 (                l1llIIIl 												)																						:										





                                                                                III1I111                              =                             lII1IlII 



                                                            else 									:									







                                                                                III1I111                        =                       l1lll1II 



                                        if III1I111 											==											lIl111II                 :                







                                                            IIIlI1l1                  =                 IllIl11I 


                                        if III1I111 									==									II1lllII 								:								









                                                            IIIlI1l1 											=											III1IlII 






                                        if IIIlI1l1                                ==                               lIlIlIll 													:													




                                                            llI1IlI1                 =                lI1l11lI 
                                                            if lI11I1l1                  (                 l1111Ill                            ,                           IlI1II1l 																)																												:												







                                                                                llI1IlI1 											=											lllII1ll 



                                                            else                        :                       









                                                                                llI1IlI1 									=									II111lIl 



                                                            if llI1IlI1 														==														l11I1IlI                           :                          



                                                                                if llllIIII 														(														random 												.												random                 (                											)											                        ,                        I1IIII11                                 )                                                          :                          






                                                                                                    llI1IlI1                                =                               lllII1ll 



                                                                                else                           :                          









                                                                                                    llI1IlI1                           =                          IlllIIl1 






                                                            if llI1IlI1                  ==                 l1IllI1l                               :                              








                                                                                IIIlI1l1                     =                    I1l1ll1I 
                                                            if llI1IlI1                    ==                   l1IlI111 													:													





                                                                                IIIlI1l1                              =                             Il11I111 









                                        if IIIlI1l1 													==													l1II1ll1 								:								






                                                            IllI111I                  =                 									[									l1Il1l11 											,											I1IlIII1 										,										IIIIl1II                 ,                IllII1ll 										,										II1Ill1I 												,												I1IllIII 									,									l1Ill1lI                    ,                   lIIl1lII                       ,                      l1lIl1ll 												,												Ill1l1l1                               ,                              lll1lllI 													,													l1lIll1I 									,									lIlll1lI                               ,                              I1l1ll11                      ,                     llIl1I11 										]										






                                                            input_handler                          .                         bind                           (                          l11ll1I1 									(									random 																.																choice                     (                    IllI111I 													)													                     )                                           ,                      IlIIlIl1 														(														random                          .                         choice 										(										IllI111I                  )                 										)										                       )                       







                                        if IIIlI1l1 								==								I111lIII 												:												

                                                            pass 








def I11I1Ill                      (                     I1III1II                      ,                     Il1III11                      )                     															:															









                    global block_pick 

                    global fullscreen 

                    global camera_pos 


                    IIll1I11 															=															l1l111l1 





                    llI1lIl1 								=								IlIIlIll 







                    if not IllI1IIl                                 :                                



                                        llI1lIl1 									=									ll11IlIl 









                    else                     :                    








                                        llI1lIl1                      =                     l1l1II1I 









                    if llI1lIl1                          ==                         IIlIIll1 													:													









                                        if not IlllI1lI 															:															








                                                            llI1lIl1                       =                      lIlIl1ll 







                                        else                           :                          



                                                            llI1lIl1 											=											Il111l1I 
                    if llI1lIl1                     ==                    Il111l1I                         :                        
                                        IIll1I11                          =                         IllIIII1 





                    if llI1lIl1 															==															l11Il1l1 											:											



                                        IIll1I11                      =                     ll11lllI 


                    if IIll1I11                                 ==                                IllllII1 													:													



                                        lIlIl1lI                           =                          Il1l1IIl 




                                        l1111II1                          =                         IlIIl1I1 



                                        if not IIII11lI 										(										I1III1II 										,										l1Il1l11 												)												                    :                    







                                                            l1111II1                  =                 IIl11lll 




                                        else                          :                         









                                                            l1111II1 																=																l1IlI111 



                                        if l1111II1 															==															II111lIl 								:								






                                                            if not isplayerkilled                 :                







                                                                                l1111II1 												=												l1l1IIIl 

                                                            else                             :                            

                                                                                l1111II1 								=								llIlIIIl 







                                        if l1111II1 												==												I11IIIll 										:										
                                                            lIlIl1lI 											=											l1lIIllI 









                                        if l1111II1 												==												IIllIlI1                     :                    






                                                            lIlIl1lI 									=									I11I11lI 

                                        if lIlIl1lI 								==								IIII11ll 										:										





                                                            if not Il11lIll 										.										llIl11II 																(																lI1IIIlI                                )                               															:															







                                                                                lIlIl1lI                        =                       IIIlIIlI 








                                                            else                              :                             






                                                                                lIlIl1lI 								=								I1l1IIIl 
                                        if lIlIl1lI                          ==                         IIIlIIlI                              :                             






                                                            IIll1I11                     =                    IlllIIl1 


                                        if lIlIl1lI                          ==                         I1l1IIIl 										:										
                                                            IIll1I11 								=								Il11l111 

                    if IIll1I11                  ==                 ll11lllI 										:										




                                        global escmenuenabled 


                                        IllI1IlI                                =                               I1IllllI 







                                        lIIl11ll                  =                 lIlI11I1 



                                        if IIII11lI 											(											escmenuenabled                             ,                            fuck_up 										(										llllIlIl 										)																						)																											:															



                                                            lIIl11ll 													=													I1lIIl1I 

                                        else                  :                 




                                                            lIIl11ll                     =                    lIlI1II1 


                                        if lIIl11ll 										==										lIlIl111 													:													





                                                            if not IllllII1 														:														
                                                                                lIIl11ll 												=												II11IlIl 


                                                            else 																:																







                                                                                lIIl11ll                         =                        III1IlII 





                                        if lIIl11ll 													==													IllIlII1                 :                








                                                            IllI1IlI                           =                          III1ll1I 








                                        if lIIl11ll                               ==                              l111l1lI 												:												


                                                            IllI1IlI 															=															l1II1II1 


                                        if IllI1IlI                             ==                            l1II1II1                         :                        





                                                            l1l1I1l1                        =                       IIlIl11l 


                                                            if not l1111l1l 									(									l1I1lII1 											)											                           :                           







                                                                                l1l1I1l1                         =                        l1I1lIlI 




                                                            else 																:																
                                                                                l1l1I1l1 									=									Ill1lI1l 





                                                            if l1l1I1l1 											==											llI111ll 									:									








                                                                                if not I1llll11                                 (                                Il11l1II                       )                                             :                       






                                                                                                    l1l1I1l1                                =                               I1llI11I 






                                                                                else 												:												









                                                                                                    l1l1I1l1 															=															lIlIl1ll 


                                                            if l1l1I1l1 																==																I1I1llI1 									:									

                                                                                IllI1IlI 															=															IIlI1I11 


                                                            if l1l1I1l1                       ==                      lll1IIll                              :                             

                                                                                IllI1IlI                              =                             III1ll1I 









                                        if IllI1IlI 													==													ll1I11lI                     :                    





                                                            escmenu 										.										hideMenu                  (                                             )                            






                                                            player 										.										enabled                       =                      fuck_up                    (                   l1llIIl1 															)															









                                                            escmenuenabled 												=												fuck_up 									(									lIIIIIII                         )                        




                                        if IllI1IlI 									==									IllIIII1 									:									






                                                            escmenu                   .                  showMenu                       (                                         )                   








                                                            player 												.												enabled 												=												fuck_up                   (                  III1IIl1                   )                  







                                                            escmenuenabled                    =                   fuck_up                           (                          l1llIIl1                 )                







                    if IIll1I11                     ==                    IlllI1lI 												:												









                                        pass 






                    IlII1llI 													=													l1ll1Il1 









                    Il1II11I 												=												ll1Ill11 








                    if not l1111l1l                       (                      l1lI1II1                          )                         													:													







                                        Il1II11I 											=											l1lIIllI 



                    else                    :                   


                                        Il1II11I 															=															lll11IIl 


                    if Il1II11I                       ==                      lll11IIl 								:								







                                        if not IIII11lI                    (                   I1III1II 															,															IIl11III 													)													                           :                           



                                                            Il1II11I 															=															Il1llI11 




                                        else                   :                  









                                                            Il1II11I                                =                               I1lll11I 




                    if Il1II11I                                 ==                                ll1I11lI 															:															



                                        IlII1llI                      =                     lll11111 
                    if Il1II11I                        ==                       lIII1III 									:									




                                        IlII1llI                                 =                                IIIIIlI1 






                    if IlII1llI                     ==                    IIIIIlI1 												:												

                                        l11ll1Il 															=															lllII1ll 
                                        if not IlII1l11                       :                      






                                                            l11ll1Il 								=								I1l1III1 



                                        else                           :                          








                                                            l11ll1Il                          =                         lIl1I1ll 

                                        if l11ll1Il 										==										IlIlIll1 															:															


                                                            if not Il11lIll                      .                     llIl11II 												(												l1IllI1I                            )                           														:														

                                                                                l11ll1Il 																=																l1l1l11I 



                                                            else                 :                







                                                                                l11ll1Il                     =                    IllIlIll 


                                        if l11ll1Il 								==								I1IIlIIl 												:												




                                                            IlII1llI                    =                   lIlIl111 








                                        if l11ll1Il 													==													l1II1II1                     :                    





                                                            IlII1llI                     =                    lII1IlII 





                    if IlII1llI 														==														I1IllllI 											:											







                                        pass 








                    if IlII1llI                      ==                     lIlIl111                       :                      

                                        PyneQuit 													(													                )                
                    lII1llll                    =                   Ill1I11l 





                    ll1II1l1 													=													II1IlII1 






                    if not I1llll11                   (                  IllI1l11 										)										                          :                          

                                        ll1II1l1                 =                l1II1ll1 






                    else                          :                         





                                        ll1II1l1                          =                         IlIlllII 



                    if ll1II1l1 													==													lIl11llI                                 :                                

                                        if not Il11lIll 											.											llIl11II                 (                lIlI111I                   )                  									:									




                                                            ll1II1l1                                =                               l111l1lI 







                                        else                        :                       



                                                            ll1II1l1                           =                          II11111I 









                    if ll1II1l1                        ==                       III1IlII                         :                        







                                        lII1llll                           =                          llIIlI1I 

                    if ll1II1l1                          ==                         III1ll1I 												:												







                                        lII1llll 													=													II11Illl 








                    if lII1llll                     ==                    l111lII1 													:													





                                        II1lIlI1                            =                           I1lIl1ll 
                                        if lI11I1l1 										(										Il111ll1 									,									IlI111II 								)																	:									




                                                            II1lIlI1 															=															IIlI1I11 





                                        else 											:											





                                                            II1lIlI1 														=														ll1II1ll 








                                        if II1lIlI1 									==									IllIIII1 									:									



                                                            if IIII11lI 									(									I1III1II 									,									IIIIl1II 																)																                 :                 








                                                                                II1lIlI1                                 =                                I1lllIIl 







                                                            else                      :                     









                                                                                II1lIlI1                       =                      ll1II1ll 







                                        if II1lIlI1                               ==                              llIIlI1I 								:								




                                                            lII1llll                    =                   IIIlIIlI 









                                        if II1lIlI1                       ==                      ll1II1ll                              :                             

                                                            lII1llll 															=															II1llllI 








                    if lII1llll 															==															II1llllI                         :                        








                                        respawn                             (                                               )                   






                    if lII1llll 											==											IIIlIIlI                        :                       








                                        pass 



                    lIlll11I 								=								lIl111II 


                    l111II1I 															=															I1I1llI1 






                    if not llIIIll1 									:									




                                        l111II1I                   =                  lll11111 






                    else                        :                       







                                        l111II1I 									=									IllIIII1 
                    if l111II1I 								==								lI11lIIl 											:											
                                        if IIII11lI 																(																I1III1II 														,														IllII1ll                     )                                     :                 









                                                            l111II1I                            =                           lll11111 









                                        else 								:								







                                                            l111II1I                              =                             Illl1I11 







                    if l111II1I 														==														lIlI1II1 								:								

                                        lIlll11I 														=														l1lIIllI 



                    if l111II1I 																==																ll1l1II1 									:									





                                        lIlll11I                             =                            lIl1I1ll 







                    if lIlll11I                                ==                               l11IlI1I                   :                  





                                        lll1lIl1 									=									IIIll1Il 

                                        if not l1111l1l 																(																l1I1l1lI                               )                                                      :                        






                                                            lll1lIl1 																=																lIl1IIIl 









                                        else                               :                              





                                                            lll1lIl1                     =                    I1l1IllI 




                                        if lll1lIl1                               ==                              I1l1IllI                        :                       









                                                            if not llI1II11                        :                       


                                                                                lll1lIl1 											=											lII11l1I 

                                                            else                   :                  
                                                                                lll1lIl1                      =                     IllIll1l 




                                        if lll1lIl1 													==													IllIll1l                 :                
                                                            lIlll11I 															=															Illl1II1 
                                        if lll1lIl1                           ==                          l1II1ll1 										:										







                                                            lIlll11I 									=									IlIlIll1 








                    if lIlll11I 															==															lII11l1I 																:																






                                        pass 


                    if lIlll11I                             ==                            I1l1I111                        :                       


                                        player                    .                   damage 																(																l111I11I                                 )                                






                    lI1llllI                 =                I1l1I11I 









                    II1I1I1I                          =                         II11IlIl 







                    if IlIIII1l                   (                  lI1Il1Il 												,												lII11l1I                                 )                                																:																








                                        II1I1I1I 													=													llll11II 

                    else                                :                               








                                        II1I1I1I 									=									II111I1I 








                    if II1I1I1I                          ==                         llIII1lI                                 :                                








                                        if IIII11lI 													(													I1III1II                           ,                          II1Ill1I 									)									                            :                            






                                                            II1I1I1I                  =                 lIIIl11l 








                                        else                        :                       







                                                            II1I1I1I                             =                            I11lI11l 
                    if II1I1I1I 													==													IlIl1II1                    :                   
                                        lI1llllI 									=									I1l1II1l 




                    if II1I1I1I                         ==                        Ill11llI                             :                            
                                        lI1llllI                        =                       II11111I 








                    if lI1llllI                         ==                        ll1I11lI 											:											








                                        IlIll1I1 																=																IIlI111I 








                                        if IlIIII1l                   (                  lIlI11I1 													,													IIIlIlIl 											)																											:																




                                                            IlIll1I1                      =                     I1IlIIll 



                                        else                                 :                                
                                                            IlIll1I1                                =                               l11l1lII 
                                        if IlIll1I1 															==															ll11lllI 												:												



                                                            if not l1l1lIl1                  :                 



                                                                                IlIll1I1                               =                              llIII1lI 

                                                            else 														:														







                                                                                IlIll1I1 																=																Illl1III 
                                        if IlIll1I1 											==											IIIll1Il                              :                             








                                                            lI1llllI 									=									lllI1l1l 

                                        if IlIll1I1 														==														l11l1lII                     :                    





                                                            lI1llllI                   =                  IIlI111I 









                    if lI1llllI                              ==                             l1I11IlI 																:																


                                        pass 






                    if lI1llllI                     ==                    IIlI111I 																:																




                                        block_pick                         =                        IlI11ll1 
                    I1I1lIII 								=								ll1II1ll 








                    lII1IllI 											=											lllI1l1l 


                    if not llllIIII                                (                               I111l1Il 									,									Il11lI1l 															)															                             :                             







                                        lII1IllI                       =                      l11lI1l1 







                    else                          :                         




                                        lII1IllI                  =                 IlI1I1I1 









                    if lII1IllI                               ==                              llIllIlI                       :                      




                                        if not IIII11lI                                (                               I1III1II 									,									I1IllIII                  )                                           :                          


                                                            lII1IllI                               =                              IllIlII1 









                                        else                              :                             




                                                            lII1IllI                  =                 IllIll1l 






                    if lII1IllI 																==																l1llllI1                                :                               


                                        I1I1lIII 											=											llIIlI1I 




                    if lII1IllI 								==								lIllllII                          :                         









                                        I1I1lIII 														=														llI1l1II 





                    if I1I1lIII 													==													I1lllIIl                  :                 

                                        lll11Ill 														=														I1l1I1lI 






                                        if not ll1I11II 												(												IlIl1II1                       ,                      I1llll1l 												)																						:										

                                                            lll11Ill                       =                      l1lIlI1l 






                                        else 											:											


                                                            lll11Ill                            =                           ll1I11lI 








                                        if lll11Ill 														==														II111I1I 									:									


                                                            if not lI11I1l1                          (                         Il1llI11                          ,                         lI1II11l 										)										                              :                              

                                                                                lll11Ill                            =                           Ill111l1 








                                                            else 																:																

                                                                                lll11Ill                             =                            l11I1I1l 





                                        if lll11Ill 														==														llII1llI                               :                              









                                                            I1I1lIII                       =                      l1111llI 







                                        if lll11Ill 													==													l11I1I1l                    :                   







                                                            I1I1lIII 											=											IIllIlI1 









                    if I1I1lIII 														==														II1l11Il 																:																









                                        pass 
                    if I1I1lIII                        ==                       Il11l111 																:																
                                        block_pick                               =                              l1l1II1I 






                    I1111IIl                           =                          Il1IIlII 







                    l11I1111 												=												l1lIlI1l 






                    if lI11I1l1 											(											I11IIIll                             ,                            I1I11Il1 															)																													:														

                                        l11I1111 														=														I1lll11I 


                    else 									:									








                                        l11I1111 															=															Il11l111 







                    if l11I1111                     ==                    I111l111                       :                      

                                        if IIII11lI 								(								I1III1II 								,								l1Ill1lI 								)																			:											




                                                            l11I1111                  =                 I1lllIl1 

                                        else 													:													
                                                            l11I1111 																=																Il1l1IlI 








                    if l11I1111 									==									Il1l1IlI                              :                             





                                        I1111IIl 															=															lll1I1II 




                    if l11I1111                                 ==                                Ill1I11I 													:													




                                        I1111IIl                                 =                                II1l1lI1 
                    if I1111IIl 										==										llll1IlI                            :                           









                                        Il1I1Il1 														=														Ill1I11I 





                                        if not l1111l1l                     (                    lI1ll111                       )                                           :                     



                                                            Il1I1Il1                         =                        IllIlIll 







                                        else                       :                      
                                                            Il1I1Il1                  =                 III1ll1I 


                                        if Il1I1Il1                           ==                          Ill1IIIl                              :                             






                                                            if not l1111l1l                                 (                                I1lI1I1I                                )                                                               :                                



                                                                                Il1I1Il1                          =                         lIlI1ll1 


                                                            else                      :                     


                                                                                Il1I1Il1                                =                               llIllIlI 


                                        if Il1I1Il1                        ==                       IlI1I1I1 															:															


                                                            I1111IIl                   =                  I1lll11I 






                                        if Il1I1Il1                           ==                          l1II1II1                                :                               





                                                            I1111IIl                              =                             l1l1Il1l 

                    if I1111IIl                             ==                            I111l111 											:											









                                        block_pick 											=											l1l1Il1l 



                    if I1111IIl 								==								l1l1Il1l                                 :                                







                                        pass 


                    lI1lIlll                           =                          IIlIIll1 


                    IIIIlIII                           =                          Ill1I11I 

                    if not l1111l1l 									(									llll1IlI 											)											                             :                             

                                        IIIIlIII                          =                         l1I1lIlI 



                    else 															:															








                                        IIIIlIII                             =                            l1IIl1ll 








                    if IIIIlIII 												==												I11Il111 												:												









                                        if not Il11lIll 															.															llIl11II 								(								l1III11I                  )                                          :                         





                                                            IIIIlIII 										=										Il1I1lll 








                                        else 										:										





                                                            IIIIlIII 										=										IIl1l11I 






                    if IIIIlIII                       ==                      Il1lIlI1                                 :                                





                                        lI1lIlll                  =                 Il11l111 






                    if IIIIlIII                               ==                              lIIl1lI1                           :                          






                                        lI1lIlll 																=																l1I11II1 


                    if lI1lIlll 								==								II1III1I                    :                   





                                        Il1IIIl1 									=									IlllIIl1 





                                        if IIII11lI 								(								I1III1II                  ,                 lIIl1lII 												)												                    :                    




                                                            Il1IIIl1 													=													IlI1I1I1 







                                        else 														:														




                                                            Il1IIIl1                      =                     lI11lIIl 

                                        if Il1IIIl1 														==														IIl11I1I                                 :                                





                                                            if not I1llll11 										(										IIl111I1 													)																						:									
                                                                                Il1IIIl1                    =                   IllllII1 








                                                            else 											:											





                                                                                Il1IIIl1 																=																lIllllII 





                                        if Il1IIIl1                               ==                              lIllllII 															:															

                                                            lI1lIlll                        =                       ll11lllI 




                                        if Il1IIIl1 									==									IllllII1                           :                          




                                                            lI1lIlll 									=									lllI1ll1 








                    if lI1lIlll 																==																Il1l1IlI                      :                     

                                        pass 

                    if lI1lIlll                               ==                              lIllllII                      :                     







                                        block_pick                  =                 lIl1lII1 







                    l1IlIlIl 																=																ll1lll1l 





                    ll11llII 											=											l1II1II1 


                    if IIII11lI 									(									I1III1II                                 ,                                llllI1lI 														)																									:											

                                        ll11llII 													=													Il111l1I 



                    else 											:											
                                        ll11llII 													=													IIIIIlII 









                    if ll11llII                         ==                        ll1lIIIl 														:														

                                        if not l1111l1l                          (                         llIIIIlI 								)																		:										

                                                            ll11llII                                 =                                l1l1II1I 


                                        else 												:												








                                                            ll11llII                        =                       l1l11Il1 




                    if ll11llII 									==									IIllIl11                         :                        






                                        l1IlIlIl 													=													lI1IlI11 



                    if ll11llII                     ==                    Il11l1II 															:															






                                        l1IlIlIl 													=													IIl1I1Il 




                    if l1IlIlIl 													==													l1I1lII1 									:									






                                        lll1l1I1 								=								I11Il111 

                                        if not I1llll11                         (                        ll1llIl1 																)																									:									



                                                            lll1l1I1 											=											IlIIII1I 



                                        else 												:												





                                                            lll1l1I1                         =                        llllI1l1 









                                        if lll1l1I1                     ==                    llllI1l1 											:											



                                                            if lIl1I11I                              (                             llIllIlI                 ,                Ill11I11                    )                                       :                    
                                                                                lll1l1I1                               =                              IIlIl11l 



                                                            else 												:												

                                                                                lll1l1I1 														=														I1lIl1ll 
                                        if lll1l1I1                 ==                II1lIIll                     :                    


                                                            l1IlIlIl 								=								I1l11lll 









                                        if lll1l1I1                             ==                            II11IllI                       :                      







                                                            l1IlIlIl                           =                          II111lIl 
                    if l1IlIlIl                 ==                lIllIIll 															:															

                                        pass 







                    if l1IlIlIl 										==										lIll1I1l                      :                     






                                        block_pick                           =                          l1lI1II1 

                    l1lIl1I1 										=										l1IllI1I 




                    ll1lIll1 									=									IIl1l111 







                    if IIII11lI                     (                    I1III1II 																,																I1lIlI1I 									)									                             :                             







                                        ll1lIll1                            =                           I1lll11I 
                    else                                :                               

                                        ll1lIll1                              =                             IlI1lllI 









                    if ll1lIll1 										==										l1lIIllI 																:																







                                        if IIII11lI 												(												IIIIIII1                                ,                               llIIlI1I 								)																					:													



                                                            ll1lIll1 															=															l1llIll1 






                                        else 														:														





                                                            ll1lIll1 											=											I1l1III1 




                    if ll1lIll1 									==									II1III1I 															:															








                                        l1lIl1I1                           =                          l11I1I1l 




                    if ll1lIll1 												==												l1l1lllI 											:											







                                        l1lIl1I1 								=								l1lIlI1l 


                    if l1lIl1I1 															==															IlI11llI                              :                             








                                        lIllIIIl                       =                      IIlIIll1 




                                        if llllIIII                                (                               l1I11ll1                 ,                I11lI11l                                 )                                                  :                  

                                                            lIllIIIl                                =                               IIIlll11 


                                        else 								:								






                                                            lIllIIIl                                 =                                IIl11I1I 





                                        if lIllIIIl 														==														IIl11I1I                                :                               

                                                            if llllIIII                            (                           lI11llll 																,																II1I11ll 									)																			:										








                                                                                lIllIIIl                              =                             II1l1Il1 




                                                            else                            :                           

                                                                                lIllIIIl                                 =                                lIII1lIl 







                                        if lIllIIIl                           ==                          lllIIlll                      :                     








                                                            l1lIl1I1 								=								II1IlII1 






                                        if lIllIIIl 								==								IIl111I1 													:													









                                                            l1lIl1I1 																=																l11I1I1l 
                    if l1lIl1I1 																==																IllIlI1l                                :                               

                                        pass 







                    if l1lIl1I1                          ==                         III1ll1I                  :                 




                                        block_pick                             =                            II11Illl 







                    lIIII1I1                       =                      IIll1IlI 


                    l1II1lll 								=								IllIlIll 







                    if not l1lI1lI1                            :                           
                                        l1II1lll                               =                              ll1111lI 





                    else                                 :                                


                                        l1II1lll 										=										IlI11ll1 





                    if l1II1lll                 ==                II11IIlI                                :                               






                                        if IIII11lI 								(								I1III1II 									,									lll1lllI 									)																									:																
                                                            l1II1lll 								=								IlI1I1I1 






                                        else                   :                  




                                                            l1II1lll 								=								IllllII1 






                    if l1II1lll                             ==                            lI11lIIl                     :                    

                                        lIIII1I1                         =                        l111I1I1 





                    if l1II1lll 														==														ll1111lI                                :                               







                                        lIIII1I1                           =                          ll11III1 

                    if lIIII1I1 															==															lll1I1II 												:												



                                        I111lIlIII 									=									Il111l1I 








                                        if llllIIII 														(														IIIlI1 													,													IIlIl1I1 															)															                          :                          


                                                            I111lIlIII                      =                     IlllI1lI 

                                        else 								:								


                                                            I111lIlIII                    =                   l1llIll1 







                                        if I111lIlIII 								==								ll1Ill11                          :                         



                                                            if lIl1I11I 											(											IIIlIlIl                     ,                    IllI1IIl                           )                                           :                 







                                                                                I111lIlIII                  =                 IlIlIll1 



                                                            else                               :                              






                                                                                I111lIlIII 									=									l1l1lllI 



                                        if I111lIlIII                    ==                   lII1lIlI                         :                        





                                                            lIIII1I1 								=								lll1l1ll 


                                        if I111lIlIII 								==								l1l1lllI                       :                      









                                                            lIIII1I1                                 =                                l11111ll 






                    if lIIII1I1                  ==                 II11IIlI 										:										






                                        block_pick 								=								IllllII1 








                    if lIIII1I1 									==									lll1l1ll 								:								

                                        pass 






                    III11lI1                        =                       II1I11ll 


                    Il1l1lll 																=																l1111llI 
                    if not I1llll11 								(								l1llIIll 															)																											:												
                                        Il1l1lll                             =                            lIII111l 








                    else                           :                          
                                        Il1l1lll                          =                         IIIll1Il 



                    if Il1l1lll                             ==                            l1lIlI1l                          :                         




                                        if not I1llll11 														(														IIl1I1Il 															)																												:													





                                                            Il1l1lll 									=									I1l1I11I 







                                        else                         :                        





                                                            Il1l1lll 												=												I1111IlI 
                    if Il1l1lll                    ==                   IIl1III1                                :                               







                                        III11lI1                    =                   lIlI11I1 





                    if Il1l1lll                                ==                               lI1l11lI                             :                            







                                        III11lI1                 =                I1I11IIl 




                    if III11lI1                        ==                       Il111IIl 											:											







                                        Illl11ll                         =                        I1l1ll1I 

                                        if not IIII11lI                          (                         I1III1II 															,															I11l11ll 																)																                      :                      

                                                            Illl11ll                     =                    IllIll1l 







                                        else 										:										



                                                            Illl11ll 									=									IllI1l11 









                                        if Illl11ll 											==											lII1IlII                          :                         


                                                            if not l1111l1l                               (                              lIlIlIll                    )                   															:															

                                                                                Illl11ll                 =                IllI1l11 








                                                            else                      :                     


                                                                                Illl11ll 															=															I1llll1l 

                                        if Illl11ll                      ==                     II1lIIll                                :                               








                                                            III11lI1 												=												lllI1l1l 

                                        if Illl11ll 										==										lIll1I1l 								:								









                                                            III11lI1                           =                          l1l1IlIl 









                    if III11lI1 										==										l1l1IlIl 													:													








                                        block_pick 																=																lIl1I1ll 






                    if III11lI1 													==													l1I1lII1                       :                      


                                        pass 


                    IIllll11                          =                         IlllIIl1 
                    II11III1 									=									IlIIIlIl 





                    if not IIII11lI 									(									l1lI11Il                      ,                     llIIlI1I                 )                									:									

                                        II11III1 														=														ll1lll1l 







                    else                             :                            









                                        II11III1 										=										I1llI11I 




                    if II11III1 								==								l1I1lIlI                      :                     







                                        l1IIll11 													=													I1lll11I 









                                        if not IIII11lI                             (                            I1III1II                                ,                               Il1I1lI1                            )                                             :                  
                                                            l1IIll11                   =                  l1ll1III 









                                        else 														:														






                                                            l1IIll11                               =                              I11lI11l 





                                        if l1IIll11                           ==                          l1llIIIl 																:																


                                                            if not player                               .                              enabled 								:								









                                                                                l1IIll11                        =                       I11lI11l 


                                                            else                               :                              

                                                                                l1IIll11 																=																IlII1l11 





                                        if l1IIll11 												==												l1l1ll1I                           :                          


                                                            II11III1 															=															Illl1I11 





                                        if l1IIll11 													==													IlII1l11                              :                             

                                                            II11III1                     =                    IIlI111I 

                    if II11III1 											==											I11lI11l 								:								
                                        IIllll11 														=														I1llllIl 
                    if II11III1                          ==                         IIll1I1I                   :                  






                                        IIllll11                            =                           Il11l1II 




                    if IIllll11                            ==                           III1llI1 									:									





                                        IIIIl11I 												=												I1I11IIl 






                                        if not lI11I1l1                      (                     I1IlIIll 												,												ll1III1I 											)											                               :                               

                                                            IIIIl11I 									=									IIl1Il1l 






                                        else                        :                       




                                                            IIIIl11I                         =                        IllI1l11 







                                        if IIIIl11I 									==									lIllllll 										:										


                                                            if not I1llll11 															(															IIIlll11 									)																			:										








                                                                                IIIIl11I 															=															ll1l1I11 





                                                            else                          :                         








                                                                                IIIIl11I 																=																IIIlIIlI 









                                        if IIIIl11I 													==													II1lIIll                 :                







                                                            IIllll11 									=									IIlIl1I1 








                                        if IIIIl11I                      ==                     lll1111l 														:														









                                                            IIllll11 									=									l1I1I1Il 


                    if IIllll11                      ==                     IIlllIll                 :                









                                        player 															.															left_hand 														.														active                   (                  															)															

                    if IIllll11                  ==                 llI111ll 								:								


                                        player 											.											left_hand                       .                      passive                         (                        													)													

                    II1llll1 								=								I1IlIIll 





                    l1l11lI1 														=														l1IlI111 






                    lII1l11l                                 =                                Il111IIl 




                    if IIII11lI 															(															I1III1II 								,								ll11lI11 														)														                     :                     




                                        lII1l11l 															=															l11IlI1I 







                    else                               :                              





                                        lII1l11l 														=														IIl1llI1 






                    if lII1l11l 											==											llI1IlIl                                :                               
                                        if not player                          .                         enabled                       :                      


                                                            lII1l11l 															=															lIII1III 
                                        else                   :                  

                                                            lII1l11l                           =                          II1l1lI1 








                    if lII1l11l                  ==                 lI11llll                  :                 







                                        l1l11lI1                             =                            IllI1l11 
                    if lII1l11l 													==													lIII1III                           :                          




                                        l1l11lI1 											=											ll11III1 







                    if l1l11lI1                          ==                         I1lIl1ll 												:												


                                        if not IlI11ll1 																:																









                                                            l1l11lI1 													=													l1111Ill 


                                        else                        :                       


                                                            l1l11lI1 												=												IIlI111I 



                    if l1l11lI1                             ==                            Ill11llI 																:																
                                        II1llll1                 =                lIl1IIIl 







                    if l1l11lI1 										==										l1111Ill                  :                 









                                        II1llll1 									=									lIIl1lI1 









                    if II1llll1                           ==                          lllIII1l                              :                             








                                        l1Il11Il 												=												IlIlI111 








                                        if not l1111l1l 														(														Il1IIlII 											)																						:											





                                                            l1Il11Il 											=											lll1l1ll 








                                        else                            :                           







                                                            l1Il11Il 													=													III1IlII 









                                        if l1Il11Il 																==																l1II1ll1 										:										


                                                            if not Ill111l1 											:											




                                                                                l1Il11Il                              =                             lll1Il1I 









                                                            else                            :                           

                                                                                l1Il11Il                   =                  II11Illl 





                                        if l1Il11Il                         ==                        l1111Ill 												:												





                                                            II1llll1                        =                       l1llllI1 








                                        if l1Il11Il 									==									l111lII1 																:																



                                                            II1llll1                             =                            IlIIl1ll 



                    if II1llll1                        ==                       ll11III1 															:															







                                        player 														.														right_hand 									.									passive 								(																						)														








                    if II1llll1                 ==                I1IllllI 															:															







                                        player 																.																right_hand                              .                             active 									(									                 )                 



def III1I1I1                        (                       IIIIII1l                              )                             													:													







                    pass 










def l11l111l 												(												lI1IIII1                         )                        															:															


                    pass 










def IIIlI1Il 														(														I1Illlll 										)																		:								








                    pass 




class Pynecraft                         :                        









                    def __init__ 															(															self 									,									menu_manager 															,															world 										:										str                              ,                             username                        :                       str                         )                                                   :                           









                                        return I1I1Il1I 												(												username 											,											self                  ,                 world 																,																menu_manager 											)											

                    def update                              (                             self                               )                              													:													


                                        return III1Illl 															(															self                           )                          



                    def input                      (                     self 								,								key                   )                  												:												






                                        return I11I1Ill                           (                          key 																,																self 														)														









                    def show                        (                       self 															)																												:													




                                        return III1I1I1 												(												self 										)										






                    def hide                         (                        self 															)															                      :                      









                                        return l11l111l 										(										self 											)											






                    def killMe 											(											self 														)																									:											







                                        return IIIlI1Il 															(															self 														)														