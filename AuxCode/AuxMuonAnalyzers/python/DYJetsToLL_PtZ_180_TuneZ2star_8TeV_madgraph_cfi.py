import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
source = cms.Source ("PoolSource",fileNames = readFiles)
readFiles.extend( [
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/000FCE96-B632-E211-A8FF-003048678B0C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/06623D95-A932-E211-9406-003048678B88.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/06C75E53-AB32-E211-BD12-002618943885.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0872A30B-9832-E211-9643-002354EF3BE6.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0A08DF65-A632-E211-8EC0-003048678FEA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0A48E410-A232-E211-A56E-00261894398D.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0A70EB70-B332-E211-A00C-002618943810.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0A8E2DA4-A232-E211-8186-00261894387B.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0AA240CF-A532-E211-9AD1-002618943908.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0C5EF868-AF32-E211-885B-00304866C398.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0C6EF858-C332-E211-A630-00261894390B.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0C82961D-9D32-E211-96A0-0026189438FF.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0CC4D47E-AC32-E211-BE62-003048678F8A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0CD9FAAD-AB32-E211-9B61-002618943908.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/0E98F367-A632-E211-B54E-003048678BB2.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/124077B5-AB32-E211-8F8A-0030486792A8.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/12B09C87-A332-E211-9721-003048679182.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/12FEE2F9-A632-E211-AB75-003048679182.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/140CDFA4-9032-E211-A282-002354EF3BE4.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/14547A42-8D32-E211-98D0-00261894383B.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/14868C6D-8C32-E211-8396-001BFCDBD160.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/14EBA644-AE32-E211-87E7-001A9281174A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/14FCAE41-A732-E211-971B-00261894394B.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/162D4E45-AE32-E211-96CB-003048678ED2.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1653A2B4-A632-E211-B7BE-0026189438D2.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/169E003E-7E32-E211-A207-001A92810AB2.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/181F98F2-A432-E211-AF49-0026189438CF.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/187517CF-AC32-E211-9F22-003048678C3A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1A301C35-8F32-E211-A2C8-003048678F62.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1A3D4D05-A932-E211-9684-003048D3C010.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1ABBB40B-AE32-E211-9A00-003048679180.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1C3D6E87-9A32-E211-B804-002618943971.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1E8DCF4B-A032-E211-A05A-00304867BFAA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/1ED51ECA-A332-E211-B6FF-0026189437F0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/224D3A6A-A832-E211-8283-002618FDA28E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/2469DF36-AA32-E211-A30E-002618943919.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/24D8F731-AA32-E211-AFF5-0030486790B8.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/24DFBFF9-A432-E211-9468-003048678B26.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/24EEE04D-D032-E211-915E-0018F3D09636.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/26A9F803-A032-E211-BFD1-002354EF3BE1.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/26BA72E4-A732-E211-8862-00304867924E.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/289D4275-D532-E211-82F4-002618943954.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/2ACBC25F-A932-E211-AD13-001A928116FC.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/2AEB6C21-BE32-E211-8019-0026189438D3.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/2CD7D627-A632-E211-AB27-002354EF3BCE.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/2E7FBA2E-A832-E211-8B2E-00248C0BE01E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3055B119-F832-E211-85C4-0026189438A5.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/34A9B846-B232-E211-8EC3-002618943960.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/36C04C6E-BF32-E211-A1EC-003048FFCB96.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3AA08EAC-AB32-E211-8168-00304867906C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3AB31F89-A332-E211-A2F0-002618943845.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3C1B61D4-AC32-E211-B8BC-001A9281174A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3CB3024B-8932-E211-85EC-0018F3D096BE.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3E0AB44D-8B32-E211-93A4-00261894388F.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/3EF107EB-9E32-E211-A7DA-00261894397E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/40866455-B432-E211-917A-00261894389E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/408BFDB2-CC32-E211-92C9-002618943833.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/44736C25-9B32-E211-B442-003048678BAA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/46187FF9-AD32-E211-BCC8-003048678DA2.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/46E6B592-C432-E211-AFFF-003048FFD740.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/46FC6B61-8E32-E211-8DE6-001A928116EE.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/4ED767DF-B832-E211-A25A-003048FFCB96.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/4EFE837C-C932-E211-B24A-003048FFD720.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/50FF3FE8-9432-E211-9474-003048678D86.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/52F8FF89-A132-E211-8A26-003048678CA2.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/549BB9C9-A332-E211-A884-00261894390A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/56CCE67F-B532-E211-B7DB-0030486790BE.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/56DB3876-9F32-E211-9BFF-00261894392F.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/58746198-8732-E211-8F84-0018F3D0968A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/58A691B2-A632-E211-BCC0-003048678E8A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/58D7CE6F-A832-E211-9B9C-003048679228.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/5C4F4C2D-A132-E211-B174-00261894398A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/5CB9EB89-AE32-E211-ABF8-00261894397A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/5E9DE368-A632-E211-A197-00261894397E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/6016BDA8-BC32-E211-9E5A-00261894393F.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/6088F8AF-AD32-E211-8B26-0026189438CC.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/6698C9BD-C732-E211-89DF-001A928116B0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/687A33CE-AA32-E211-8312-0026189438C4.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/689F4F5E-A232-E211-BAAE-002618943864.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/6ABB005C-AD32-E211-B1B9-0026189438FA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/6CFF072D-A832-E211-8781-003048678FA6.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/6ED5F634-AC32-E211-B4B9-003048678F26.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/727D34CC-A332-E211-9173-003048678FA6.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/745BA3C4-9D32-E211-A90F-002618943939.root',
       #'/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/7CA651AD-A432-E211-9115-001BFCDBD130.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/7CC998B2-AD32-E211-B738-00304867918A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/7EA9AF09-A932-E211-ACA0-00248C0BE01E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/8297E48B-A532-E211-88DC-00304867D446.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/82AE6D54-AB32-E211-90E6-00304866C398.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/82CE392F-A832-E211-B679-00248C0BE01E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/84136FD6-A732-E211-9B41-00248C0BE018.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/847A336E-9932-E211-9DE7-00304867D838.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/86D0B5C2-A132-E211-AB5A-00261894382A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/88401B88-A532-E211-A8F9-002618943962.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/8A7DE5A4-AC32-E211-B7E6-001A928116EC.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/8E3E05E1-A932-E211-8755-0026189438AB.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/8EFFDEAA-A432-E211-ADB1-002618FDA265.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/90833C94-9632-E211-A020-003048678B0C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/908416F9-A632-E211-A8ED-003048678B18.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/94AA8725-AD32-E211-81BE-00261894383F.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/94DE5617-A432-E211-8963-003048FFD770.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/9637B273-AA32-E211-BF04-00304867906C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/96574850-A932-E211-A3EC-003048678B12.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/969BFBB0-BA32-E211-85B0-0026189438F4.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/9A46C197-A032-E211-A396-002618943918.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/9A81F0D5-A732-E211-918D-0030486790B8.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/9C172EE0-A932-E211-BF5D-00248C55CC3C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/9CAE7AD1-AC32-E211-8ADE-003048678BAE.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/9CB8D966-8632-E211-9847-002618943845.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A0F27EEB-A032-E211-83D2-002618943811.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A257F1C3-A832-E211-BB83-00304867918A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A42227FA-A632-E211-B791-002618943962.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A441152A-A632-E211-A23D-003048679164.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A65CBF2F-B132-E211-929E-0018F3D09704.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A66F6785-A532-E211-B144-00261894394B.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A6B7A024-A832-E211-A700-0026189438C4.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A6BC9CCA-8D32-E211-831C-003048FFD796.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/A8B09121-A632-E211-BC4C-003048679164.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/AAF16F11-A432-E211-AC84-0026189438B1.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/AC328BB0-A632-E211-ACA2-00248C65A3EC.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/ACB83286-A332-E211-872C-002618FDA248.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/ACB8A633-AA32-E211-8E00-003048678E6E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/ACC15B3E-A532-E211-B587-00261894395C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/AEF2E1FB-AB32-E211-A6B3-003048678E52.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/B2BE8740-9C32-E211-94AE-00248C55CC7F.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/B41F35CF-9332-E211-B944-0018F3D096C8.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/B4EBA0B4-A832-E211-AA6E-00261894387E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/BA9EA2BC-9F32-E211-BDDE-0026189438D6.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/BE1950BC-AF32-E211-B233-002618943882.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/BEA63B33-AC32-E211-914A-002618943985.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/BEC4F930-AA32-E211-8BC1-002618943919.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/BEDE16D1-A532-E211-B6FC-003048678AC0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/BEEEEF46-B032-E211-8ED8-0026189438D4.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/C293DADD-C632-E211-B50B-003048678EE2.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/C40E7B35-E332-E211-8C0D-003048678FD6.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/C4F6E568-8A32-E211-895A-002618943980.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/C4FC2BE8-A032-E211-BDB1-00261894387A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/C80B2627-AF32-E211-A11D-0018F3D09648.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/C88E7917-C532-E211-AA5C-003048FFCB8C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/CA303839-8232-E211-ADF6-0018F3D095EA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/CA7A9FC8-9B32-E211-91B6-002618943971.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/CAF0B209-A932-E211-8D39-00248C0BE01E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/CCC34DD7-A732-E211-AE68-003048678F78.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/CE0BF2A6-C132-E211-9028-001A92971B3C.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D27B3744-A732-E211-8C65-00248C0BE012.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D2C6BEA1-A932-E211-AE1C-003048678FA0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D4475BEB-A932-E211-B19E-003048679228.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D4C4795F-A432-E211-9402-002618943923.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D4F9F339-AC32-E211-A465-001A92810AEA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D6B0705A-9232-E211-9B40-003048FFD736.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/D6DD6B88-A532-E211-8729-002354EF3BDA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/DAA83D00-B032-E211-B2D7-001A92811738.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/DCC817DA-A732-E211-AA08-0026189438B0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/E2233EF9-A632-E211-895D-002618FDA28E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/E2A261C6-AA32-E211-A923-002618943902.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/E2ECC56B-C532-E211-A7CB-003048FFD71A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/E40B79C4-C032-E211-9538-00304867C1BA.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/E472D9E1-A932-E211-A417-0030486792F0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/EAB62F83-C232-E211-A3C2-001A92811744.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/EC6F5C00-A932-E211-8F48-002618943945.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/ECB740DB-B032-E211-9A22-002618943943.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/F2299475-AA32-E211-9757-003048678B88.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/F2D2B5E5-8332-E211-9B28-002618943974.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/F496D4CA-AA32-E211-B316-0018F3D096C0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/F692A11D-A632-E211-8B58-00248C0BE018.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/F6E8E964-A232-E211-80E7-001A92971B08.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/F83BB9B7-A832-E211-9BF0-00261894389E.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/FA29614D-9E32-E211-B5FD-002618943811.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/FCD56DCF-B132-E211-9443-003048678E8A.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/FE30EE37-A332-E211-AD88-0030486790C0.root',
       '/store/mc/Summer12_DR53X/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7C-v1/00000/FED1AA3C-A532-E211-8269-00261894387D.root' ] );
