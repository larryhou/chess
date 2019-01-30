import excel chess.xlsx, clear first
drop id

gen as = real(regexr(regexr(attack_speed, "^.+\(", ""), "s?\).*$", ""))
drop attack_speed
rename as attack_speed

gsort + cost - attack_lv1_l - life_lv1

ds, has(type numeric)
quiet foreach stat of varlist `r(varlist)' {
	sum `stat'
	local dif = r(max) - r(min)
	replace `stat' = (`stat'-r(min))/(r(max) - r(min)) if `dif' > 0
	replace `stat' = 1 if `dif' == 0
	format %6.2f `stat'
}

encode chess, gen(hero)

#delimit ;
scatter attack_lv1_h life_lv1 armor attack_speed cost hero, xsize(16) ysize(9)
xlabel(1/52, valuelabel labs(*.5))
xlabel(, angle(90) grid glw(*.5) tl(*.3))
ylabel(0(0.1)1.0, glw(*.5) labs(*.5) tl(*.3))
xtitle("")
legend(row(1) colgap(*2) size(*.5) region(c(none)))
legend(label(1 "攻击") label(2 "生命") label(3 "护甲") label(4 "攻速") label(5 "价格"))
sort(hero) c(direct = =) msize(*.35 ..)
mcolor(red green magenta blue black)
mfc(red green magenta none black)
mlw(*0.3 ..) 
lcolor(red green magenta blue black) lw(*.75 *.5 ..)
graphr(m(tiny))
;
#delimit cr
graph export dota.pdf, replace
