import FWCore.ParameterSet.Config as cms

from CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi import tpScales
from Configuration.Eras.Modifier_run2_HE_2017_cff import run2_HE_2017
from Configuration.Eras.Modifier_run2_HF_2017_cff import run2_HF_2017
from Configuration.Eras.Modifier_run3_HB_cff import run3_HB
from Configuration.Eras.Modifier_run3_common_cff import run3_common

LSParameter =cms.untracked.PSet(
HcalFeatureHFEMBit= cms.bool(False),
Min_Long_Energy= cms.double(10),#makes a cut based on energy deposited in short vrs long
    Min_Short_Energy= cms.double(10),
    Long_vrs_Short_Slope= cms.double(100.2),
    Long_Short_Offset= cms.double(10.1))


simHcalTriggerPrimitiveDigis = cms.EDProducer("HcalTrigPrimDigiProducer",
    peakFilter = cms.bool(True),
    weights = cms.vdouble(1.0, 1.0), ##hardware algo        
    weightsQIE11 = cms.PSet(
        ieta1 = cms.vint32(255, 255),
        ieta2 = cms.vint32(255, 255),
        ieta3 = cms.vint32(255, 255),
        ieta4 = cms.vint32(255, 255),
        ieta5 = cms.vint32(255, 255),
        ieta6 = cms.vint32(255, 255),
        ieta7 = cms.vint32(255, 255),
        ieta8 = cms.vint32(255, 255),
        ieta9 = cms.vint32(255, 255),
        ieta10 = cms.vint32(255, 255),
        ieta11 = cms.vint32(255, 255),
        ieta12 = cms.vint32(255, 255),
        ieta13 = cms.vint32(255, 255),
        ieta14 = cms.vint32(255, 255),
        ieta15 = cms.vint32(255, 255),
        ieta16 = cms.vint32(255, 255),
        ieta17 = cms.vint32(255, 255),
        ieta18 = cms.vint32(255, 255),
        ieta19 = cms.vint32(255, 255),
        ieta20 = cms.vint32(255, 255),
        ieta21 = cms.vint32(255, 255),
        ieta22 = cms.vint32(255, 255),
        ieta23 = cms.vint32(255, 255),
        ieta24 = cms.vint32(255, 255),
        ieta25 = cms.vint32(255, 255),
        ieta26 = cms.vint32(255, 255),
        ieta27 = cms.vint32(255, 255),
        ieta28 = cms.vint32(255, 255)
    ),

    latency = cms.int32(1),
    FG_threshold = cms.uint32(12), ## threshold for setting fine grain bit
    FG_HF_thresholds = cms.vuint32(17, 255), ## thresholds for setting fine grain bit
    ZS_threshold = cms.uint32(1),  ## threshold for setting TP zero suppression
    numberOfSamples = cms.int32(4),
    numberOfPresamples = cms.int32(2),
    numberOfSamplesHF = cms.int32(4),
    numberOfPresamplesHF = cms.int32(2),
    numberOfFilterPresamplesHBQIE11 = cms.int32(0),
    numberOfFilterPresamplesHEQIE11 = cms.int32(0),
    useTDCInMinBiasBits = cms.bool(False), # TDC information not used in MB fine grain bits
    MinSignalThreshold = cms.uint32(0), # For HF PMT veto
    PMTNoiseThreshold = cms.uint32(0),  # For HF PMT veto
    LSConfig=LSParameter,

    upgradeHF = cms.bool(False),
    upgradeHB = cms.bool(False),
    upgradeHE = cms.bool(False),

    applySaturationFix = cms.bool(False), # Apply the TP energy saturation fix for Peak Finder Algorithm only for Run3 

    # parameters = cms.untracked.PSet(
    #     FGVersionHBHE=cms.uint32(0),
    #     TDCMask=cms.uint64(0xFFFFFFFFFFFFFFFF),
    #     ADCThreshold=cms.uint32(0),
    #     FGThreshold=cms.uint32(12)
    # ),

    #vdouble weights = { -1, -1, 1, 1} //low lumi algo
    # Input digi label (_must_ be without zero-suppression!)
    inputLabel = cms.VInputTag(cms.InputTag('simHcalUnsuppressedDigis'),
                               cms.InputTag('simHcalUnsuppressedDigis')),
    inputUpgradeLabel = cms.VInputTag(
        cms.InputTag('simHcalUnsuppressedDigis:HBHEQIE11DigiCollection'),
        cms.InputTag('simHcalUnsuppressedDigis:HFQIE10DigiCollection')),
    InputTagFEDRaw = cms.InputTag("rawDataCollector"),
    overrideDBweightsAndFilterHB = cms.bool(False),
    overrideDBweightsAndFilterHE = cms.bool(False),
    RunZS = cms.bool(False),
    FrontEndFormatError = cms.bool(False), # Front End Format Error, for real data only
    PeakFinderAlgorithm = cms.int32(2),

    tpScales = tpScales,
)

run2_HE_2017.toModify(simHcalTriggerPrimitiveDigis, upgradeHE=cms.bool(True))
run2_HF_2017.toModify(simHcalTriggerPrimitiveDigis, 
                      upgradeHF=cms.bool(True),
                      numberOfSamplesHF = cms.int32(2),
                      numberOfPresamplesHF = cms.int32(1)
)
run2_HF_2017.toModify(tpScales.HF, NCTShift=cms.int32(2))
run3_HB.toModify(simHcalTriggerPrimitiveDigis, upgradeHB=cms.bool(True))
run3_common.toModify(simHcalTriggerPrimitiveDigis, applySaturationFix=cms.bool(True))
run3_HB.toModify(tpScales.HBHE, LSBQIE11Overlap=cms.double(1/16.))
