#include "Riostream.h"

void ToFmacros() {
    gStyle->SetOptStat(0);
	TH2D* hist = new TH2D("hist", "TOF histogram", 120, -100, 140, 90, 0, 9000);
//	TH2D* hist = new TH2D("hist", "TOF histogram", 120, -100, 140, 100, 0, 4000);
    ifstream in;
    in.open("./some-merry-five.txt");

    Int_t nlines = 0;
    //TFile *f = new TFile("basic.root","RECREATE");

    Float_t x, y, z, u, v, dummy;
    while (1) {
        in >> x >> y >> z >> u >> v;
        if (!in.good()) break;
        if (nlines < 5) printf("x=%8f, y=%8f, z=%8f, u=%8f, v=%8f\n", x, y, z, u, v);
//	if (u==0) {
//		dummy = u -v;
//	} else {
//		hist->Fill(u, v);
//	}
	if ((u!=0)&&(v>=0)) {
		hist->Fill(u, v);
	}
        nlines++;
    }
    
    TCanvas* canvas = new TCanvas("canvas");

    hist->SetTitle("Histogram of TOF for UT Aerogel Cherenkov Counter");
    hist->GetXaxis()->SetTitle("TOF [TDC]");
    hist->GetYaxis()->SetTitle("Sum of Pulse Areas [ADC]");
    hist->GetYaxis()->SetTitleOffset(1.2);
    canvas->cd();
    canvas->SetLogz();
    hist->Draw("colz");
    canvas->SaveAs("TOF.eps");

    in.close();
}
