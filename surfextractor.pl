#!/usr/bin/perl
#
#
# Script to collect fitting data.
#
# --------------------------------------------------------------------
# Execution
# ---------
# surf_calc.pl [nstates] [data directory name] [dipole]
# 
# [nstates] = number of states in system
# [data directory name] = name of directory where data is
#                         to be collected.
# [dipole]  = (y/n) collect dipole information
#
# --------------------------------------------------------------------
# Directories and data collecting
# -------------------------------
# $JDIR = COLUMBUS job execution directory: ./
# $LDIR = COLUMBUS listings directory:      ./LISTINGS/
# $GDIR = COLUMBUS gradients directory:     ./GRADIENTS/
# $WDIR = COLUMBUS work directory:          ./WORK/
# $PDIR = project directory:               ../[data directory name]/
#
# surf_calc.pl creates the directory ./DATA/.
# surf_calc.pl collects and appends data to the directory
# ../[data directory name]. 
# surf_calc.pl collects and places data in ./DATA/
#
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# MAIN ---------------------------------------------------------------
use strict;
use warnings;

my $JDIR = "./";
my $GDIR = "./GRADIENTS";
my $WDIR = "./WORK";
my $DDIR = "./DATA";
my $LDIR = "./LISTINGS";

# Process command line arguments. Set number of states and name of
# the project directory.
my $argc = $#ARGV + 1;
if ($argc != 3) {
    print "\nUsage: surf_calc.pl [nstates] [dir name] [dipole?]\n";
    die   "Incorrect number of input arguments.\n";
}
my $nst = $ARGV[0];
my $PDIR= "../$ARGV[1]";
my $dpc = $ARGV[2];

# Print current directory
system("pwd");

# Check to see if project directory is present
if (!-d "$PDIR") {
    die "$PDIR does not exist!\n";
}

# Check to see if mcscf converged. **Assuming output is: runls (previously runc.log)**
my $test = `grep converged runls`;
if ($test ne "") {
    die "MCSCF not converged.";
}

# Check to see if all files are available: gradients, couplings, and energy;
# then, if directed to, the dipole data.
for (my $i = 1; $i <= $nst; $i++) {
    if (!-e "$GDIR/cartgrd.drt1.state$i.sp"){
	die "$GDIR/cartgrd.drt1.state$i.sp does not exist!\n";
    }
    if ($dpc eq "y") {
	if (!-e "$LDIR/propls.ci.drt1.state$i.sp") {
	    die "$LDIR/propls.ci.drt1.state$i.sp does not exist!\n";
	}
    }
    for (my $j = $i + 1; $j <= $nst; $j++) {
	if (!-e "$GDIR/cartgrd.nad.drt1.state$i.drt1.state$j.sp"){
	    die "cartgrd.nad.drt1.state$i.drt1.state$j.sp does not exist!\n";
	}
	if ($dpc eq "y") {
	    if (!-e "$LDIR/trncils.FROMdrt1.state${i}TOdrt1.state$j") {
		die "$LDIR/trncils.FROMdrt1.state${i}TOdrt1.state$j does not exist!\n";
	    }
	}
    }
}
if (!-e "$LDIR/energy") {
    die "$LDIR/energy does not exist!\n";
}
if (!-e "$LDIR/ciudgsm.sp") {
    die "$LDIR/ciudgsm.sp does not exist!\n";
}

# Make ./DATA directory. Copy all files here. Append contents of all
# files to $PDIR/.
# geometry
system("mkdir $DDIR");
my @geom;
open (GMJ, "./geom");
@geom = grep(/\n/i, <GMJ>);
close (GMJ);
open (GEOM, ">>$PDIR/geom.all");
print GEOM @geom;
close(GEOM);
system("cp ./geom $DDIR/geom.all");
system("cp $GDIR/cartgrd*sp $DDIR/");
system("cp $LDIR/energy $DDIR/");
if ($dpc eq "y") {
    system("cp $LDIR/trncils* $DDIR/");
    system("cp $LDIR/propls.ci* $DDIR/");
}
# gradients, couplings
for (my $i = 1; $i <= $nst; $i++) {
    my @grd;
    open (CRTGD, "$GDIR/cartgrd.drt1.state$i.sp");
    @grd = grep(/\n/i, <CRTGD>);
    close(CRTGD);
    open (GRDS, ">>$PDIR/cartgrd.drt1.state$i.all");
    print GRDS @grd;
    close(GRDS);
    for (my $j = $i + 1; $j <= $nst; $j++) {
	my @cp;
	open (CRTCP, "$GDIR/cartgrd.nad.drt1.state$i.drt1.state$j.sp");
	@cp = grep(/\n/i, <CRTCP>);
	close(CRTCP);
	open (NADS, ">>$PDIR/cartgrd.nad.drt1.state$i.drt1.state$j.all");
	print NADS @cp;
	close(NADS);
    }
}
# dipoles
if ($dpc eq "y") {
    for (my $i = 1; $i <= $nst; $i++) {
	my @ddp;
	open (DPLE, "$LDIR/propls.ci.drt1.state$i.sp");
	@ddp = grep(/total   /i, <DPLE>);
	close(DPLE);
	open (DPLS, ">>$PDIR/propls.ci.drt1.state$i.all");
	print DPLS @ddp;
	close(DPLS);
	for (my $j = $i + 1; $j <= $nst; $j++) {
	    my @tdp;
	    open (TDPLE, "$LDIR/trncils.FROMdrt1.state${i}TOdrt1.state$j");
	    @tdp = grep(/total \(elec\)/, <TDPLE>);
	    close(TDPLE);
	    open (TDPLS, ">>$PDIR/trncils.FROMdrt1.state${i}TOdrt1.state$j.all");
	    print TDPLS @tdp;
	    close(TDPLS);
	}
    }
}
#energy
my @en;
open (ENRG, "$LDIR/energy");
@en = grep(/\n/i, <ENRG>);
close(ENRG);
for (my $i = 1; $i <= $nst; $i++) {
    my $enrg = 0;
    $enrg = substr($en[$i], 12, 14);
    if ($i < $nst) {
	open (ENGS, ">>$PDIR/oldenergy.all");
	print ENGS "$enrg ";
	close(ENGS);
    } else {
	open (ENGS, ">>$PDIR/oldenergy.all");
	print ENGS "$enrg\n";
	close(ENGS);
    }
}
my @enl;
open (ENRGL, "$LDIR/ciudgsm.sp");
@enl = grep(/\n/i, <ENRGL>);
close(ENRGL);
my $firstline;
my $firsttime;
$firstline = 0;
$firsttime = 0;
for (my $i = 1; $i <= @enl - 1; $i++) {
    if (index($enl[$i], "final") != -1) {
        if ($firsttime == 0) {
            $firsttime = 1;
	} elsif ($firsttime == 1) {
	    $firsttime = 2;
	    $firstline = $i + 1
	}
    }
}
for (my $i = $firstline; $i <= $firstline + $nst - 1; $i++) {
    my $enrg = 0;
    $enrg = substr($enl[$i], 19, 16);
    if ($i < $firstline + $nst - 1) {
        open (ENGSL, ">>$PDIR/energy.all");
        print ENGSL "$enrg ";
        close(ENGSL);
    } else {
        open (ENGSL, ">>$PDIR/energy.all");
        print ENGSL "$enrg\n";
        close(ENGSL);
    }
}

#---------------------------------------------------------------------

