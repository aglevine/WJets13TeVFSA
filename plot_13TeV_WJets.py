from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import math
import array
import wj_vars
import XSec

def makeQCDShape():
	data2015B = make_histo(savedir,"SingleMuon2015B","aisomjHighMt",var,lumidir,lumi)
	wjets = make_histo(savedir,"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","aisomjHighMt",var,lumidir,lumi)
	wjets.Scale(wjetsScale)
	DYJets_10to50 = make_histo(savedir,"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8", "aisomjHighMt",var,lumidir,lumi)
	DYJets_50 = make_histo(savedir,"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "aisomjHighMt",var,lumidir,lumi)
	tFullT = make_histo(savedir,"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1","aisomjHighMt",var,lumidir,lumi)
	tW = make_histo(savedir,"ST_tW_top_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1","aisomjHighMt",var,lumidir,lumi)
	tbarW = make_histo(savedir,"ST_tW_antitop_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1","aisomjHighMt",var,lumidir,lumi)

	ww = make_histo(savedir,"WW_TuneCUETP8M1_13TeV-pythia8","aisomjHighMt",var,lumidir,lumi)
	wz = make_histo(savedir,"WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","aisomjHighMt",var,lumidir,lumi)
	zz = make_histo(savedir,"ZZTo4L_13TeV-amcatnloFXFX-pythia8","aisomjHighMt",var,lumidir,lumi)

	ttbar = make_histo(savedir,"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","aisomjHighMt",var,lumidir,lumi)

	qcdShape = data2015B.Clone()
	qcdShape.Add(wjets,-1)
	qcdShape.Add(DYJets_10to50,-1)
	qcdShape.Add(DYJets_50,-1)
	qcdShape.Add(tFullT,-1)
	qcdShape.Add(tW,-1)
	qcdShape.Add(tbarW,-1)
	qcdShape.Add(ww,-1)
	qcdShape.Add(wz,-1)
	qcdShape.Add(zz,-1)

	return qcdShape
	

def yieldHisto(histo,xmin,xmax):
        binmin = int(histo.FindBin(xmin))
        binwidth = histo.GetBinWidth(binmin)
        binmax = int(xmax/binwidth)
        signal = histo.Integral(binmin,binmax)
        print "binmin" + str(binmin)
        print "binmax" + str(binmax)
        return signal

def make_histo(savedir,file_str, channel,var,lumidir,lumi,isData=False):
        histoFile = ROOT.TFile(savedir+file_str+".root")
        print histoFile
        ROOT.gROOT.cd()
        histo = histoFile.Get(channel+"/"+var).Clone()
        if (isData==False):
        	metafile = lumidir + file_str +"_weight.log"
        	f = open(metafile).read().splitlines()
        	nevents = float((f[0]).split(': ',1)[-1])
		#xsecfile = lumidir+file_str+"_xsec.txt"
		#fx  = open(xsecfile).read().splitlines()
        	#xsec = float(fx[0])
                #getXsec="XSec."+file_str.replace("-","_")
                #print getXsec
                #xsecList = eval(getXsec)
                #print xsecList
                xsec = eval("XSec."+file_str.replace("-","_"))
		efflumi = nevents/xsec
        	histo.Scale(lumi/efflumi)
        print file_str+" Integral: " + str(histo.Integral())
        return histo

##Set up style
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

savedir=argv[1]
var=argv[2]
channel=argv[3]
canvas = ROOT.TCanvas("canvas","canvas",800,800)

shape_norm = False
if shape_norm == False:
        ynormlabel = " "
else:
        ynormlabel = "Normalized to 1 "

getVarParams = "wj_vars."+var
varParams = eval(getVarParams)
xlabel = varParams[0]
binwidth = varParams[7]

legend = eval(varParams[8])
isGeV = varParams[5]
xRange = varParams[6]
wjetsScale=1
if (wjetsScale!=1):
	outfile_name = savedir+"LFV"+"_"+channel+"_"+var+"_WJetsPUFix"
else:
	outfile_name = savedir+"LFV"+"_"+channel+"_"+var
#p_wj = ROOT.TPad('p_wj','p_wj',0,0,1,1)
#p_wj.SetLeftMargin(0.2147651)
#p_wj.SetRightMargin(0.06543624)
#p_wj.SetTopMargin(0.04895105)
#p_wj.SetBottomMargin(0.1311189)
#p_wj.Draw()
#p_wj.cd()

p_wj = ROOT.TPad('p_lfv','p_lfv',0,0,1,1)
p_wj.SetLeftMargin(0.2147651)
p_wj.SetRightMargin(0.06543624)
p_wj.SetTopMargin(0.04895105)
p_wj.SetBottomMargin(0.305)
p_wj.Draw()
p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.295)
p_ratio.SetLeftMargin(0.2147651)
p_ratio.SetRightMargin(0.06543624)
p_ratio.SetTopMargin(0.04895105)
p_ratio.SetBottomMargin(0.295)
p_ratio.SetGridy()
p_ratio.Draw()
p_wj.cd()

#lumidir = savedir+"json_lumicalc/"
lumidir = savedir+"weights/"
#lumi =16.354
lumi=2000
#lumi = 25000 #25 fb-1

#qcdShape = makeQCDShape()
#qcd = qcdShape.Clone()
#qcd.Scale(0.105)

#data2015B = make_histo(savedir,"SingleMuon2015B",channel,var,lumidir,lumi,True)
#data2015B_1 = make_histo(savedir,"data__SingleMuon_Run2015B-PromptReco-v1_MINIAOD",channel,var,lumidir,lumi,True)
#data2015C = make_histo(savedir,"data__SingleMuon_Run2015C-PromptReco-v1_MINIAOD",channel,var,lumidir,lumi,True)
data2015C = make_histo(savedir,"data_SingleMuon_Run2015C_05Oct2015_25ns",channel,var,lumidir,lumi,True)
data2015D = make_histo(savedir,"data_SingleMuon_Run2015D_05Oct2015_25ns",channel,var,lumidir,lumi,True)
data2015D_v4 = make_histo(savedir,"data_SingleMuon_Run2015D_PromptReco-v4_25ns",channel,var,lumidir,lumi,True)
wjets = make_histo(savedir,"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",channel,var,lumidir,lumi)
#wjets = make_histo(savedir,"WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",channel,var,lumidir,lumi)
#wjets.Scale(1/61526.7)
#wjets = make_histo(savedir,"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_PUReweight",channel,var,lumidir,lumi)
#wjets = make_histo(savedir,"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_PUFix",channel,var,lumidir,lumi)
#wjets.Scale(wjetsScale)
#DYJets_10to50 = make_histo(savedir,"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8", channel,var,lumidir,lumi)
zjets = make_histo(savedir,"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", channel,var,lumidir,lumi)


#tFullT = make_histo(savedir,"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",channel,var,lumidir,lumi)
#tW = make_histo(savedir,"ST_tW_top_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",channel,var,lumidir,lumi)
#tS = make_histo(savedir,"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",channel,var,lumidir,lumi)
#tbarW = make_histo(savedir,"ST_tW_antitop_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",channel,var,lumidir,lumi)

ww = make_histo(savedir,"WW_TuneCUETP8M1_13TeV-pythia8",channel,var,lumidir,lumi)
wz = make_histo(savedir,"WZ_TuneCUETP8M1_13TeV-pythia8",channel,var,lumidir,lumi)
zz = make_histo(savedir,"ZZ_TuneCUETP8M1_13TeV-pythia8",channel,var,lumidir,lumi)

#ttbar = make_histo(savedir,"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",channel,var,lumidir,lumi)
ttbar = make_histo(savedir,"TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",channel,var,lumidir,lumi)

#qcd30to50 = make_histo(savedir,"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",channel,var,lumidir,lumi)
#qcd50to80 = make_histo(savedir,"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",channel,var,lumidir,lumi)
#qcd80to120 = make_histo(savedir,"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",channel,var,lumidir,lumi)
#qcd120to170 = make_histo(savedir,"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",channel,var,lumidir,lumi)

#qcd = qcd30to50.Clone()
#qcd.Add(qcd50to80)
#qcd.Add(qcd80to120)
#qcd.Add(qcd120to170)

#data2015B=data2015B_1.Clone()
data=data2015C.Clone()
data.Add(data2015D)
data.Add(data2015D_v4)

#singlet = tFullT.Clone()
#singlet.Add(tW)
#singlet.Add(tbarW)
#singlet.Add(tS)

diboson = ww.Clone()
diboson.Add(wz)
diboson.Add(zz)
print "binwidth: " + str(binwidth)

data.Rebin(binwidth)
#qcd.Rebin(binwidth)
wjets.Rebin(binwidth)
zjets.Rebin(binwidth)
ttbar.Rebin(binwidth)
#singlet.Rebin(binwidth)
diboson.Rebin(binwidth)

data.SetMarkerStyle(8)
data.SetMarkerSize(1)
#qcd.SetFillColor(ROOT.EColor.kBlue)
#qcd.SetLineColor(ROOT.EColor.kBlue)
#qcd.SetLineWidth(1)
#qcd.SetMarkerSize(0)
wjets.SetFillColor(ROOT.EColor.kMagenta-10)
wjets.SetLineColor(ROOT.EColor.kMagenta+4)
wjets.SetLineWidth(1)
wjets.SetMarkerSize(0)
zjets.SetFillColor(ROOT.EColor.kOrange-4)
zjets.SetLineColor(ROOT.EColor.kOrange+4)
zjets.SetLineWidth(1)
zjets.SetMarkerSize(0)
ttbar.SetFillColor(40)
ttbar.SetLineColor(ROOT.EColor.kBlack)
ttbar.SetLineWidth(1)
ttbar.SetMarkerSize(0)
diboson.SetFillColor(ROOT.EColor.kRed+2)
diboson.SetLineColor(ROOT.EColor.kRed+4)
diboson.SetLineWidth(1)
diboson.SetMarkerSize(0)
#singlet.SetFillColor(ROOT.EColor.kGreen-2)
#singlet.SetLineColor(ROOT.EColor.kGreen+4)
#singlet.SetLineWidth(1)
#singlet.SetMarkerSize(0)

#wjets.Scale(225892.45)

WJStack = ROOT.THStack("stack","")
WJStack.Add(diboson)
WJStack.Add(zjets)
#WJStack.Add(qcd)
WJStack.Add(ttbar)
#WJStack.Add(singlet)
WJStack.Add(wjets)

#print "fw!!: " + str((yieldHisto(data2015B,50,200)-yieldHisto(diboson,50,200)-yieldHisto(zjets,50,200)-yieldHisto(ttbar,50,200)-yieldHisto(singlet,50,200)-yieldHisto(qcd,50,200))/(yieldHisto(wjets,50,200)))

#print channel + " data - MC: (low Mt) " + str(yieldHisto(data2015B,0,50)-yieldHisto(diboson,0,50)-yieldHisto(zjets,0,50)-yieldHisto(ttbar,0,50)-yieldHisto(singlet,0,50)-yieldHisto(wjets,0,50))

maxWJStack = WJStack.GetMaximum()
maxData=data.GetMaximum()
maxHist = max(maxWJStack,maxData)

WJStack.SetMaximum(maxHist*1.20)
WJStack.Draw('hist')
data.Draw("sames,E1")

legend.AddEntry(diboson,'EWK Di-Boson',"f")
legend.AddEntry(zjets,'Z+Jets','f')
#legend.AddEntry(qcd,'QCD','f')
legend.AddEntry(ttbar,'t#bar{t}')
#legend.AddEntry(singlet,'Single Top')
legend.AddEntry(wjets,'W+Jets','f')

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

xbinLength = wjets.GetBinWidth(1)
widthOfBin = binwidth*xbinLength

if isGeV:
        ylabel = ynormlabel + " Events / " + str(int(widthOfBin)) + " GeV"
else:
        ylabel = ynormlabel  + " Events / " + str(widthOfBin)

legend.Draw('sames')
WJStack.GetXaxis().SetTitle(xlabel)
WJStack.GetXaxis().SetNdivisions(510)
#WJStack.GetXaxis().SetTitleOffset(3.0)
#WJStack.GetXaxis().SetLabelOffset(3.0)
WJStack.GetXaxis().SetLabelSize(0.035)
#WJStack.GetYaxis().SetTitle(ylabel)
WJStack.GetYaxis().SetTitleOffset(1.40)
WJStack.GetYaxis().SetLabelSize(0.035)

if ("mMt" in var):
	WJStack.GetXaxis().SetRangeUser(0,200)
if ("jetVeto20" in var):
        WJStack.GetXaxis().SetRangeUser(1,5)
if ("m_j" in var):
	WJStack.GetXaxis().SetRangeUser(0.2,4)
if ("Mass" in var):
        WJStack.GetXaxis().SetRangeUser(0.2,1000)
#else:
#	WJStack.GetXaxis().SetRangeUser(0,xRange)
WJStack.GetXaxis().SetTitle(xlabel)

xbinLength = wjets.GetBinWidth(1)
widthOfBin = binwidth*xbinLength

size = wjets.GetNbinsX()
#build tgraph of systematic bands
xUncert = array.array('f',[])
yUncert = array.array('f',[])
exlUncert = array.array('f',[])
exhUncert = array.array('f',[])
eylUncert = array.array('f',[])
eyhUncert = array.array('f',[])
binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)

for i in range(1,size+1):
        stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+ttbar.GetBinContent(i)+diboson.GetBinContent(i)
        wjetsBinContent = wjets.GetBinContent(i)
        xUncert.append(wjets.GetBinCenter(i))
        yUncert.append(stackBinContent)
        exlUncert.append(binLength/2)
        exhUncert.append(binLength/2)
        eylUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+ttbar.GetBinError(i)+diboson.GetBinError(i))
        eyhUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+ttbar.GetBinError(i)+diboson.GetBinError(i))
        xUncertVec = ROOT.TVectorF(len(xUncert),xUncert)
        yUncertVec = ROOT.TVectorF(len(yUncert),yUncert)
        exlUncertVec = ROOT.TVectorF(len(exlUncert),exlUncert)
        exhUncertVec = ROOT.TVectorF(len(exhUncert),exhUncert)
        eylUncertVec = ROOT.TVectorF(len(eylUncert),eylUncert)
        eyhUncertVec = ROOT.TVectorF(len(eyhUncert),eyhUncert)
        systErrors = ROOT.TGraphAsymmErrors(xUncertVec,yUncertVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(31)
latexStr = "%.1f pb^{-1}, #sqrt{s} = 13 TeV"%(lumi)
latex.DrawLatex(0.9,0.96,latexStr)
latex.SetTextAlign(11)
latex.DrawLatex(0.25,0.96,"CMS preliminary")

systErrors.SetFillStyle(3001)
systErrors.SetFillColor(ROOT.EColor.kGray+3)
systErrors.SetMarkerSize(0)
#systErrors.Draw('sames,E2')
#legend.AddEntry(systErrors,'Bkg. Uncertainty')


p_ratio.cd()
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
ratio = data.Clone()
mc = wjets.Clone()
mc.Add(zjets)
mc.Add(ttbar)
mc.Add(diboson)
#mc.Add(singlet)
#mc.Add(qcd)
mc.Scale(-1)
ratio.Add(mc)
mc.Scale(-1)
ratio.Divide(mc)
ratio.Draw("E1")
if ("mMt" in var):
	ratio.GetXaxis().SetRangeUser(0,200)
if ("jetVeto20" in var):
	ratio.GetXaxis().SetRangeUser(1,5)
ratio.GetXaxis().SetTitle(xlabel)
ratio.GetXaxis().SetTitleSize(0.12)
ratio.GetXaxis().SetNdivisions(510)
ratio.GetXaxis().SetTitleOffset(1.1)
ratio.GetXaxis().SetLabelSize(0.12)
ratio.GetXaxis().SetLabelFont(42)
ratio.GetYaxis().SetNdivisions(505)
ratio.GetYaxis().SetLabelFont(42)
ratio.GetYaxis().SetLabelSize(0.1)
ratio.GetYaxis().SetRangeUser(-1,1)
ratio.GetYaxis().SetTitle("#frac{Data-MC}{MC}")
ratio.GetYaxis().CenterTitle(1)
ratio.GetYaxis().SetTitleOffset(0.4)
ratio.GetYaxis().SetTitleSize(0.12)
ratio.SetTitle("")


canvas.SaveAs(outfile_name+"_WeightFix.png")
