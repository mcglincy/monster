#!/usr/bin/perl
while (<>)
{
        chomp;
        if($_ =~ /^\@tel/)
        {
                $room=$_;
                $room=~ s/.* //;
                #print "$room\n";
        }
        elsif ($_ =~ /\@open/)
        {
                #print "$_\n";
                $loc=$_;
                $loc=~ s/.* //;
                $dir=$_;
                $dir=~s/.*;//;
                $dir=~s/ .*//;
                print "$room -> $loc [label=\"$dir\"];\n";
        }
}