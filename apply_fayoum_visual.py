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


p = root / "src/game/fayoum.ts"
s = p.read_text(encoding="utf-8")

# Fill both sides of the corridor with continuous, varied mid-rise blocks.
needle = """  outer.meshes.forEach((m, i) => {"""
dense = """  // Dense two-sided Dar El Salam frontage: one building about every 20 metres.
  for (let i = 0; i < pts.length; i += 4) {
    const p = pts[i];
    const nxt = pts[(i + 8) % pts.length];
    const bend = Math.abs(((nxt.yaw - p.yaw + Math.PI * 3) % (Math.PI * 2)) - Math.PI);
    if (bend > 0.22) continue;
    const hsh = Math.abs(Math.sin(i * 12.9898) * 43758.5453) % 1;
    const rx = Math.cos(p.yaw);
    const rz = -Math.sin(p.yaw);
    for (const side of [-1, 1]) {
      const idx = (i + (side > 0 ? 1 : 0)) % 5;
      if (outer.counts[idx] >= 95) continue;
      const floors = 3 + Math.floor(hsh * 5);
      const height = floors * 2.75 + (hsh > 0.7 ? 1.2 : 0);
      const depth = 8.5 + hsh * 3.5;
      const width = 5.4 + (1 - hsh) * 2.2;
      dummy.position.set(p.x + rx * side * (ROAD_HALF + 7.2 + hsh * 0.8), height / 2, p.z + rz * side * (ROAD_HALF + 7.2 + hsh * 0.8));
      dummy.rotation.set(0, p.yaw + (hsh - 0.5) * 0.08, 0);
      dummy.scale.set(width, height, depth);
      dummy.updateMatrix();
      outer.meshes[idx].setMatrixAt(outer.counts[idx]++, dummy.matrix);
    }
  }

  outer.meshes.forEach((m, i) => {"""
if s.count(needle) != 1:
    raise SystemExit(f"fayoum.ts: expected one building finalize point, found {s.count(needle)}")
s = s.replace(needle, dense, 1)

# Add identifiable, correctly ordered civic/shopfront labels and a market cluster.
needle = """  const bumpMat = new THREE.MeshStandardMaterial({ map: bumpTexture() ?? undefined, roughness: 0.55 });"""
visuals = """  // Grounded wayfinding for the documented Fayoum Street landmarks.
  const landmarkLabel = (index: number, lat: number, title: string, sub: string, bg: string, width = 5.8) => {
    const p = spot(track.stops[index].s, lat);
    const map = shopTex(title, sub, bg, "#ffffff");
    if (!map) return;
    const sign = new THREE.Mesh(
      new THREE.PlaneGeometry(width, 1.55),
      new THREE.MeshStandardMaterial({ map, roughness: 0.7, side: THREE.DoubleSide }),
    );
    sign.position.set(p.x, 4.15, p.z);
    sign.rotation.y = p.yaw;
    scene.add(sign);
  };
  landmarkLabel(1, 12.8, "محطة مترو دار السلام", "الخط الأول", "#a52b2b", 6.6);
  landmarkLabel(2, 12.8, "مكتب صحة دار السلام", "خدمات المواطنين", "#176b56", 5.8);
  landmarkLabel(3, 12.8, "سنترال دار السلام", "الشبكة الرئيسية", "#174c78", 5.8);
  landmarkLabel(5, 13.8, "مجمع مدارس شارع الفيوم", "مدرسة جمال عبد الناصر", "#174c78", 7.2);
  landmarkLabel(8, 13.4, "سوق الخضار", "خلف المدرسة المعمارية", "#1e8449", 5.8);
  landmarkLabel(9, 13.0, "منطقة الملاءة", "نهاية شارع الفيوم", "#5d4037", 5.8);

  // Produce market cluster behind the architecture school: striped canopies, poles and crates.
  {
    const roofMats = ["#1e8449", "#f0b429", "#c0392b", "#f4f1e7"].map(
      (color) => new THREE.MeshStandardMaterial({ color, roughness: 0.82, side: THREE.DoubleSide }),
    );
    const poleMat = new THREE.MeshStandardMaterial({ color: "#55504a", roughness: 0.8, metalness: 0.15 });
    const crateMats = ["#a86b32", "#c9842a", "#8e5a2b"].map(
      (color) => new THREE.MeshStandardMaterial({ color, roughness: 0.9 }),
    );
    const fruitMats = ["#c0392b", "#e67e22", "#2f6b3a", "#f4d03f"].map(
      (color) => new THREE.MeshStandardMaterial({ color, roughness: 0.72 }),
    );
    for (let k = 0; k < 5; k++) {
      const p = track.sample(track.stops[8].s + (k - 2) * 4.2);
      const rx = Math.cos(p.yaw);
      const rz = -Math.sin(p.yaw);
      const cx = p.x + rx * 15.2;
      const cz = p.z + rz * 15.2;
      const stall = new THREE.Group();
      stall.position.set(cx, 0, cz);
      stall.rotation.y = p.yaw;
      const roof = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.16, 2.8), roofMats[k % roofMats.length]);
      roof.position.y = 2.65;
      stall.add(roof);
      for (const x of [-1.72, 1.72]) {
        for (const z of [-1.2, 1.2]) {
          const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.06, 2.65, 6), poleMat);
          pole.position.set(x, 1.32, z);
          stall.add(pole);
        }
      }
      for (let c = 0; c < 3; c++) {
        const crate = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.52, 0.7), crateMats[(k + c) % crateMats.length]);
        crate.position.set(-1.0 + c * 1.0, 0.38, 1.05);
        stall.add(crate);
        const fruit = new THREE.Mesh(new THREE.SphereGeometry(0.19, 7, 6), fruitMats[(k + c) % fruitMats.length]);
        fruit.position.set(-1.0 + c * 1.0, 0.78, 1.05);
        stall.add(fruit);
      }
      scene.add(stall);
    }
  }

  const bumpMat = new THREE.MeshStandardMaterial({ map: bumpTexture() ?? undefined, roughness: 0.55 });"""
if s.count(needle) != 1:
    raise SystemExit(f"fayoum.ts: expected one bump section, found {s.count(needle)}")
s = s.replace(needle, visuals, 1)
p.write_text(s, encoding="utf-8")


# Keep storefront labels generic unless a specific business name is verified.
replace_once("src/game/fayoum.ts",
"""  { name: "صيدلية الشفاء", sub: "٢٤ ساعة", bg: "#c0392b", fg: "#ffffff" },""",
"""  { name: "صيدلية", sub: "خدمة يومية", bg: "#c0392b", fg: "#ffffff" },""")
replace_once("src/game/fayoum.ts",
"""  { name: "قهوة الحج", sub: "شاي · قهوة", bg: "#6e2c00", fg: "#f6f1e7" },""",
"""  { name: "قهوة", sub: "شاي · قهوة", bg: "#6e2c00", fg: "#f6f1e7" },""")
replace_once("src/game/fayoum.ts",
"""  // brick / concrete top band
  g.fillStyle = "#9a4f3a";
  g.fillRect(0, 0, 512, 90);
  for (let y = 4; y < 86; y += 14) {
    g.fillStyle = y % 28 === 4 ? "#7e3e2e" : "#b05a45";
    g.fillRect(0, y, 512, 9);
    g.fillStyle = "#5e3024";
    g.fillRect(0, y + 9, 512, 3);
    // brick offsets
    for (let x = (y % 28 === 4 ? 0 : 28); x < 512; x += 56) {
      g.fillStyle = "rgba(0,0,0,0.12)";
      g.fillRect(x, y, 2, 12);
    }
  }""",
"""  // Weathered exposed-concrete parapet, common on unfinished upper floors.
  g.fillStyle = "#8f8c83";
  g.fillRect(0, 0, 512, 90);
  for (let i = 0; i < 95; i++) {
    const shade = 95 + (i * 17) % 55;
    g.fillStyle = "rgba(110,108,102,0.18)";
    g.fillRect((i * 47) % 512, (i * 29) % 88, 10 + (i % 24), 3 + (i % 7));
  }
  g.fillStyle = "#6f6d66";
  g.fillRect(0, 82, 512, 8);
  g.fillStyle = "rgba(235,228,211,0.24)";
  g.fillRect(0, 4, 512, 5);""")


# Move building frontages to the outer sidewalk edge instead of leaving a wide empty setback.
replace_once("src/game/fayoum.ts",
"""dummy.position.set(p.x + rx * side * (22.5 + hsh * 3), height / 2, p.z + rz * side * (22.5 + hsh * 3));""",
"""dummy.position.set(p.x + rx * side * (ROAD_HALF + 7.2 + hsh * 0.8), height / 2, p.z + rz * side * (ROAD_HALF + 7.2 + hsh * 0.8));""")

print("Applied Fayoum Street corridor and visual frontage changes.")
