

def level_from_xp(xp):
  return int(xp / 1000)


# [GLOBAL]
# PROCEDURE DieChangeExperience(Th : INTEGER; My : INTEGER; VAR Stat : StatType);
# VAR
#   Mylevel, R : INTEGER;
# BEGIN
#   Th := Th DIV 1000;  (* making it the level, not the exp *)
#   Mylevel := My DIV 1000;
#   IF (Mylevel = 0) OR (Mylevel < Th) THEN
#   BEGIN
#     IF (((TH/2) + 1.5 - Mylevel) > 0) THEN
#       R := Round(1000*((Th/2) + 1.5 - Mylevel))
#     ELSE R := Round(1000*(1/(Mylevel+(Mylevel-th))));
#   END
#   ELSE
#   BEGIN
#     IF (Mylevel >= Th) AND (Mylevel < 10) AND ((Mylevel - Th) < 3)THEN
#       R := Round(1000*(1/(Mylevel+(Mylevel-Th))))
#    ELSE
#      R := 0;
#    END;
#    ChangeExp(R, Stat.Log, Stat.Experience);
# END;
def kill_xp(killer_xp, victim_xp):
  killer_level = level_from_xp(killer_xp)
  victim_level = level_from_xp(victim_xp)
  levels_above = killer_level - victim_level
  amt = 0
  if killer_level == 0 or killer_level < victim_level:
    multiplier = (victim_level / 2) + 1.5 - killer_level
    if multiplier < 0:
      multiplier = 1 / (killer_level + levels_above)
    amt = int(round(1000 * multiplier))
  elif killer_level >= victim_level and killer_level < 10 and levels_above < 3:
    amt = int(round(1000 * (1 / (killer_level + levels_above))))
  return amt  