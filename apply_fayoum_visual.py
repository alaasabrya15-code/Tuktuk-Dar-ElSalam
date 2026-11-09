from pathlib import Path
import sys

root = Path(sys.argv[1])

def replace_once(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, found {count}: {old[:70]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

replace_once("src/game/track.ts",
"""  bumps: number[];
  sample:""",
"""  bumps: number[];
  streetLength: number;
  sample:""")

replace_once("src/game/track.ts",
"""  const straight = 680;
  const radius = 34;
  const segStraight = 190;
  const segArc = 32;""",
"""  // 2.2 km outbound Fayoum Street corridor; the parallel return leg preserves the driving loop.
  const straight = 2200;
  const radius = 18;
  const segStraight = 440;
  const segArc = 36;""")

replace_once("src/game/track.ts",
"""  const stops = STOP_NAMES.map((name, i) => ({
    name,
    s: ((i + 0.06) / STOP_NAMES.length) * total,
  }));

  const tollS = stops[0].s + 6;
  const radarS = [0.16, 0.41, 0.73].map((t) => t * total);
  const gasS = total * 0.58;
  const bumps = [0.11, 0.28, 0.47, 0.66, 0.84].map((t) => t * total);""",
"""  const stopProgress = [0.012, 0.095, 0.19, 0.29, 0.41, 0.57, 0.65, 0.74, 0.83, 0.94, 0.988];
  const stops = STOP_NAMES.map((name, i) => ({ name, s: stopProgress[i] * straight }));

  const tollS = stops[0].s + 6;
  const radarS = [0.24, 0.62, 0.87].map((t) => t * straight);
  const gasS = straight * 0.48;
  // Speed bumps are concentrated by the school-complex section.
  const bumps = [0.565, 0.585, 0.605, 0.625].map((t) => t * straight);""")

replace_once("src/game/track.ts",
"""  return { pts, total, stops, tollS, radarS, gasS, bumps, sample, project };""",
"""  return { pts, total, stops, tollS, radarS, gasS, bumps, streetLength: straight, sample, project };""")

replace_once("src/game/types.ts",
"""export const STOP_NAMES = [
  "كوبري دار السلام",
  "موقف كوبري دار السلام",
  "محطة مترو دار السلام",
  "مكتب الصحة",
  "سنترال دار السلام",
  "مجمع مدارس شارع الفيوم",
  "مدرسة جمال عبد الناصر",
  "الإدارة التعليمية",
  "سناتر الدروس",
  "سوق الخضار خلف المدرسة المعمارية",
  "منطقة الملاءة",
  "موقف نهاية شارع الفيوم",
  "شارع أحمد زكي",
  "امتداد شارع الفيوم ناحية المعادي",
];""",
"""export const STOP_NAMES = [
  "كوبري دار السلام",
  "محطة مترو دار السلام",
  "مكتب الصحة",
  "سنترال دار السلام الرئيسي",
  "الإدارة التعليمية",
  "مجمع مدارس شارع الفيوم",
  "مدرسة جمال عبد الناصر",
  "سناتر الدروس الخصوصية",
  "سوق الخضار خلف المدرسة المعمارية",
  "الملاءة - نهاية شارع الفيوم",
  "شارع أحمد زكي",
];""")
replace_once("src/game/engine.ts",
"""new THREE.CircleGeometry(980, 64)""",
"""new THREE.CircleGeometry(2600, 96)""")

replace_once("src/game/engine.ts",
"""  const wrongs: Wrong[] = [
    { s: 80, speed: 7.2, lat: 6.4 },
    { s: 260, speed: 6.4, lat: -6.2 },
    { s: 480, speed: 7.6, lat: 6.6 },
    { s: 720, speed: 6.2, lat: -5.8 },
    { s: 940, speed: 7, lat: 6.1 },
  ];""",
"""  const wrongs: Wrong[] = [
    { s: track.streetLength * 0.12, speed: 7.2, lat: 6.4 },
    { s: track.streetLength * 0.31, speed: 6.4, lat: -6.2 },
    { s: track.streetLength * 0.49, speed: 7.6, lat: 6.6 },
    { s: track.streetLength * 0.72, speed: 6.2, lat: -5.8 },
    { s: track.streetLength * 0.91, speed: 7, lat: 6.1 },
  ];""")

replace_once("src/game/street.ts",
"""  footbridge(scene, track, track.total * 0.5);
""", "")

replace_once("src/game/street.ts",
"""  hang(track.stops[1].s - 8, 10.2, ["موقف كوبري دار السلام", "السيدة زينب", "الجيزة", "الزهراء · المعادي", "الهرم · التحرير"], "#0b3a82");
  hang(track.stops[6].s - 4, 11.4, ["مترو دار السلام", "الخط الأول"], "#c0392b");
  hang(track.total * 0.5 - 10, -11, ["كوبري المشاة", "ناحية السوق"], "#3d4650");
  hang(track.stops[12].s, 11, ["شارع المحجر", "مدخل الحي"], "#1c2833", "#f0b429", 3.6, 1.8);
  hang(track.stops[13].s - 12, 10.6, ["شارع أحمد زكي", "آخر شارع الفيوم"], "#1c2833", "#f0b429", 4.4, 2);""",
"""  hang(track.stops[1].s - 8, 10.2, ["محطة مترو دار السلام", "الخط الأول"], "#a52b2b");
  hang(track.stops[5].s - 8, 11.4, ["مجمع مدارس شارع الفيوم", "مدرسة جمال عبد الناصر"], "#174c78");
  hang(track.stops[9].s - 8, 10.6, ["الملاءة", "نهاية شارع الفيوم"], "#1c2833", "#f0b429", 4.4, 2);
  hang(track.stops[10].s - 8, 10.6, ["شارع أحمد زكي", "حدائق المعادي"], "#1c2833", "#f0b429", 4.4, 2);""")

p = root / "src/game/street.ts"
s = p.read_text(encoding="utf-8")
old = """  for (let i = 20; i < pts.length; i += 46) {
    const p = pts[i];
    const bend = Math.abs(((pts[(i + 8) % pts.length].yaw - p.yaw + Math.PI * 3) % (Math.PI * 2)) - Math.PI);
    if (bend > 0.16) continue;
    hang(p.s, 12.2, ["شارع الفيوم", "حي دار السلام"], "#16324f", "#f6f1e7", 3.4, 1.5);
  }
"""
if old not in s:
    raise SystemExit("street.ts: repeated fabricated overhead signs block not found")
p.write_text(s.replace(old, "", 1), encoding="utf-8")

p = root / "src/game/fayoum.ts"
s = p.read_text(encoding="utf-8")
a = s.find("  put(11, 11.6, (g) => {")
if a < 0:
    raise SystemExit("fayoum.ts: old stop-11 sign cluster not found")
b = s.find("\n  {\n    const p = spot(track.gasS", a)
if b < 0:
    raise SystemExit("fayoum.ts: gas point after stop-11 cluster not found")
s = s[:a] + s[b:]

a = s.find("  {\n    const sm = track.sample(track.total * 0.22);")
if a < 0:
    raise SystemExit("fayoum.ts: unsupported mosque block not found")
b = s.find("\n  const bumpMat", a)
if b < 0:
    raise SystemExit("fayoum.ts: bump section after mosque block not found")
s = s[:a] + s[b:]
p.write_text(s, encoding="utf-8")

print("Applied Fayoum Street corridor changes.")
