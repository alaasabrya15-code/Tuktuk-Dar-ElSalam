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
  landmarkLabel(4, 12.8, "الإدارة التعليمية", "دار السلام", "#5d4037", 5.8);
  landmarkLabel(5, 13.8, "مجمع مدارس شارع الفيوم", "مدرسة جمال عبد الناصر", "#174c78", 7.2);
  landmarkLabel(6, 13.8, "مدرسة جمال عبد الناصر", "مدرسة ثانوية بنات", "#174c78", 6.2);
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

  // Parked private cars along the curb, as seen in the street reference photos.
  {
    const bodyMats = ["#f4f1ea", "#c7c4bc", "#8b9297", "#6b747b", "#b8a58d", "#263746"].map(
      (color) => new THREE.MeshStandardMaterial({ color, roughness: 0.58, metalness: 0.08 }),
    );
    const glassMat = new THREE.MeshStandardMaterial({ color: "#253c49", roughness: 0.22, metalness: 0.16 });
    const tireMat = new THREE.MeshStandardMaterial({ color: "#17191c", roughness: 0.88 });
    const lampMat = new THREE.MeshStandardMaterial({ color: "#f6e8bd", emissive: "#c6a66c", emissiveIntensity: 0.12 });
    for (let i = 0; i < 12; i++) {
      const sm = track.sample(105 + i * 176);
      const side = i % 2 === 0 ? -1 : 1;
      const car = new THREE.Group();
      car.position.set(
        sm.x + Math.cos(sm.yaw) * side * (ROAD_HALF - 1.15),
        0,
        sm.z - Math.sin(sm.yaw) * side * (ROAD_HALF - 1.15),
      );
      car.rotation.y = sm.yaw;
      const body = new THREE.Mesh(new THREE.BoxGeometry(1.72, 0.82, 4.05), bodyMats[i % bodyMats.length]);
      body.position.y = 0.72;
      const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.42, 0.76, 2.05), glassMat);
      cabin.position.set(0, 1.43, -0.12);
      car.add(body, cabin);
      for (const x of [-0.83, 0.83]) {
        for (const z of [-1.28, 1.28]) {
          const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.18, 10), tireMat);
          wheel.rotation.z = Math.PI / 2;
          wheel.position.set(x, 0.36, z);
          car.add(wheel);
        }
      }
      for (const x of [-0.55, 0.55]) {
        const headlamp = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.18, 0.06), lampMat);
        headlamp.position.set(x, 0.82, 2.04);
        car.add(headlamp);
      }
      scene.add(car);
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


# Re-map the pre-existing landmark meshes to the corrected real-world stop order.
replace_once("src/game/fayoum.ts", """  put(1, 10.6,""", """  put(0, 18.5,""")
replace_once("src/game/fayoum.ts", """  put(2, 13.4,""", """  put(22, 13.4,""")
replace_once("src/game/fayoum.ts", """  put(3, 13.2,""", """  put(2, 13.2,""")
replace_once("src/game/fayoum.ts", """  put(22, 13.4,""", """  put(3, 13.4,""")
replace_once("src/game/fayoum.ts", """  put(4, 13.4,""", """  put(44, 13.4,""")
replace_once("src/game/fayoum.ts", """  put(5, 13.6,""", """  put(6, 13.6,""")
replace_once("src/game/fayoum.ts", """  put(44, 13.4,""", """  put(5, 13.4,""")
replace_once("src/game/fayoum.ts", """  put(6, 12.2,""", """  put(4, 12.2,""")

p = root / "src/game/fayoum.ts"
s = p.read_text(encoding="utf-8")
a = s.find("  put(7, 12.6, (g) => {")
if a < 0:
    raise SystemExit("fayoum.ts: old clinic landmark not found")
b = s.find("\n  put(8, 12.4,", a)
if b < 0:
    raise SystemExit("fayoum.ts: next landmark after clinic not found")
s = s[:a] + s[b:]
a = s.find("  put(9, 11.8, (g) => {")
if a < 0:
    raise SystemExit("fayoum.ts: unverified bakery landmark not found")
b = s.find("\n  put(10, 12.2,", a)
if b < 0:
    raise SystemExit("fayoum.ts: next landmark after bakery not found")
s = s[:a] + s[b:]
p.write_text(s, encoding="utf-8")



# Correct the doubled frontage pass: use one two-sided instancing pass only.
p = root / "src/game/fayoum.ts"
s = p.read_text(encoding="utf-8")
a = s.find("  // Dense two-sided Dar El Salam frontage:")
b = s.find("\n  outer.meshes.forEach((m, i) => {", a)
if a < 0 or b < 0:
    raise SystemExit("fayoum.ts: duplicate frontage pass not found")
s = s[:a] + s[b+1:]
old = "if (outer.counts[idx] < 95 && i % 5 === 0 && side === outward) {"
if s.count(old) != 1:
    raise SystemExit("fayoum.ts: original one-sided building placement not found")
s = s.replace(old, "if (outer.counts[idx] < 95 && i % 5 === 0) {", 1)
s = s.replace("    const outward = Math.sign(p.x * rx + p.z * rz) || 1;\n", "", 1)

# Replace generic blocks with the correct civic buildings for the stop sequence.
a = s.find("  put(3, 13.4, (g) => {")
b = s.find("\n  put(5, 13.4,", a)
if a < 0 or b < 0:
    raise SystemExit("fayoum.ts: central/health landmark region not found")
civic = """  // Dar El Salam metro entrance: stairs, ticket hall and red line fascia.
  put(1, 13.2, (g) => {
    const hall = new THREE.Mesh(new THREE.BoxGeometry(8.5, 3.1, 5.2), white);
    hall.position.set(0, 1.55, -1.2);
    const canopy = new THREE.Mesh(new THREE.BoxGeometry(9.2, 0.24, 5.8), red);
    canopy.position.set(0, 3.2, -1.2);
    const stairMat = new THREE.MeshStandardMaterial({ color: "#9c9b96", roughness: 0.88 });
    for (let k = 0; k < 7; k++) {
      const step = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.16, 0.48), stairMat);
      step.position.set(0, 0.12 + k * 0.16, 1.0 + k * 0.48);
      g.add(step);
    }
    const signMap = shopTex("محطة مترو دار السلام", "الخط الأول", "#a52b2b", "#ffffff");
    if (signMap) {
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(7.4, 1.25), new THREE.MeshStandardMaterial({ map: signMap, side: THREE.DoubleSide }));
      sign.position.set(0, 3.9, 1.55);
      g.add(sign);
    }
    g.add(hall, canopy);
  });

  // Health office: low public-service building with a visible red cross.
  put(2, 13.2, (g) => {
    const block = new THREE.Mesh(new THREE.BoxGeometry(12, 6.2, 8), stone);
    block.position.set(0, 3.1, -0.5);
    const fascia = new THREE.Mesh(new THREE.BoxGeometry(12.15, 0.72, 8.12), green);
    fascia.position.set(0, 5.25, -0.5);
    const door = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2.8, 0.18), dark);
    door.position.set(0, 1.4, 3.58);
    const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.34, 1.2, 0.12), white);
    crossV.position.set(-4.4, 4.35, 3.62);
    const crossH = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.34, 0.12), white);
    crossH.position.set(-4.4, 4.35, 3.62);
    for (const x of [-2.8, 2.8]) {
      const win = new THREE.Mesh(new THREE.BoxGeometry(1.45, 1.35, 0.12), teal);
      win.position.set(x, 3.2, 3.62);
      g.add(win);
    }
    g.add(block, fascia, door, crossV, crossH);
  });

  // Main telephone exchange: wider civic facade, rooftop aerials and a WE sign.
  put(3, 13.4, (g) => {
    const block = new THREE.Mesh(new THREE.BoxGeometry(15, 10, 9), concrete);
    block.position.y = 5;
    const band = new THREE.Mesh(new THREE.BoxGeometry(15.2, 1.05, 9.2), teal);
    band.position.set(0, 7.5, 0);
    const entry = new THREE.Mesh(new THREE.BoxGeometry(2.1, 3.2, 0.2), dark);
    entry.position.set(0, 1.6, 4.58);
    for (const x of [-5.2, -2.6, 2.6, 5.2]) {
      const win = new THREE.Mesh(new THREE.BoxGeometry(1.45, 1.65, 0.14), white);
      win.position.set(x, 4.4, 4.6);
      g.add(win);
    }
    const aerial = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 4.8, 7), dark);
    aerial.position.set(5.7, 12.4, -2.4);
    const dish = new THREE.Mesh(new THREE.SphereGeometry(1.05, 10, 8), white);
    dish.scale.set(1, 0.22, 1);
    dish.position.set(-4.8, 10.9, -2.4);
    const signMap = shopTex("WE", "سنترال دار السلام", "#5b2c83", "#ffffff");
    if (signMap) {
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 1.5), new THREE.MeshStandardMaterial({ map: signMap, side: THREE.DoubleSide }));
      sign.position.set(0, 8.2, 4.66);
      g.add(sign);
    }
    g.add(block, band, entry, aerial, dish);
  });
"""
s = s[:a] + civic + s[b:]

# Replace the former stair prop with the education administration building.
a = s.find("  put(4, 12.2, (g) => {")
b = s.find("\n\n  put(8, 12.4,", a)
if a < 0 or b < 0:
    raise SystemExit("fayoum.ts: education administration prop not found")
admin = """  put(4, 12.2, (g) => {
    const block = new THREE.Mesh(new THREE.BoxGeometry(13, 8.5, 8.5), stone);
    block.position.set(0, 4.25, -0.4);
    const band = new THREE.Mesh(new THREE.BoxGeometry(13.2, 0.85, 8.7), "#174c78" as unknown as THREE.Material);
    band.position.set(0, 6.8, -0.4);
    const entrance = new THREE.Mesh(new THREE.BoxGeometry(1.8, 3.1, 0.18), dark);
    entrance.position.set(0, 1.55, 3.92);
    for (const x of [-4.5, -2.4, 2.4, 4.5]) {
      for (const y of [3.1, 5.5]) {
        const win = new THREE.Mesh(new THREE.BoxGeometry(1.25, 1.05, 0.12), teal);
        win.position.set(x, y, 3.95);
        g.add(win);
      }
    }
    const signMap = shopTex("الإدارة التعليمية", "دار السلام", "#174c78", "#ffffff");
    if (signMap) {
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(7.2, 1.4), new THREE.MeshStandardMaterial({ map: signMap, side: THREE.DoubleSide }));
      sign.position.set(0, 7.45, 4.05);
      g.add(sign);
    }
    g.add(block, band, entrance);
  });"""
# use a proper material for the fascia instead of a string cast
admin = admin.replace('new THREE.MeshStandardMaterial({ color: "#174c78", roughness: 0.65 }) as unknown as THREE.Material', 'new THREE.MeshStandardMaterial({ color: "#174c78", roughness: 0.65 })')
admin = admin.replace('new THREE.Mesh(new THREE.BoxGeometry(13.2, 0.85, 8.7), "#174c78" as unknown as THREE.Material)', 'new THREE.Mesh(new THREE.BoxGeometry(13.2, 0.85, 8.7), new THREE.MeshStandardMaterial({ color: "#174c78", roughness: 0.65 }))')
s = s[:a] + admin + s[b:]

# The end stop is a road transition, not a fabricated cafe landmark.
a = s.find("  put(10, 12.2, (g) => {")
b = s.find("const p = spot(track.gasS", a)
c = s.rfind("  {", a, b) if b >= 0 else -1
if a >= 0 and b >= 0 and c >= 0:
    s = s[:a] + s[c:]
elif a >= 0:
    raise SystemExit("fayoum.ts: cafe landmark / gas station boundary not found")

# Add the documented three-building St Mina / St Augustine church compound.
church = """
  // Church compound confirmed on Fayoum Street. Exact frontage chainage is approximate
  // until a georeferenced street-level pin is available.
  {
    const p = spot(track.streetLength * 0.35, 16.2);
    const compound = new THREE.Group();
    compound.position.set(p.x, 0, p.z);
    compound.rotation.y = p.yaw;
    const plaster = new THREE.MeshStandardMaterial({ color: "#e4d8c4", roughness: 0.86 });
    const trim = new THREE.MeshStandardMaterial({ color: "#b79d79", roughness: 0.78 });
    const roof = new THREE.MeshStandardMaterial({ color: "#8c8173", roughness: 0.82 });
    const glass = new THREE.MeshStandardMaterial({ color: "#426a78", roughness: 0.28, metalness: 0.12 });
    const main = new THREE.Mesh(new THREE.BoxGeometry(10.5, 8.2, 13), plaster);
    main.position.set(0, 4.1, 0);
    const naveRoof = new THREE.Mesh(new THREE.BoxGeometry(10.8, 0.5, 13.3), roof);
    naveRoof.position.set(0, 8.35, 0);
    const apse = new THREE.Mesh(new THREE.BoxGeometry(5.4, 5.2, 5.2), plaster);
    apse.position.set(0, 2.6, -8.8);
    const admin = new THREE.Mesh(new THREE.BoxGeometry(6.2, 5.6, 6.5), trim);
    admin.position.set(-9.1, 2.8, -1.2);
    const service = new THREE.Mesh(new THREE.BoxGeometry(6.8, 4.8, 6), plaster);
    service.position.set(9.0, 2.4, -1.5);
    compound.add(main, naveRoof, apse, admin, service);
    for (const x of [-3.4, 0, 3.4]) {
      const win = new THREE.Mesh(new THREE.BoxGeometry(1.15, 2.15, 0.14), glass);
      win.position.set(x, 4.5, 6.58);
      compound.add(win);
    }
    const door = new THREE.Mesh(new THREE.BoxGeometry(1.8, 3.2, 0.2), trim);
    door.position.set(0, 1.6, 6.62);
    compound.add(door);
    const arch = new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.14, 8, 18, Math.PI), trim);
    arch.position.set(0, 3.35, 6.7);
    arch.rotation.z = Math.PI;
    compound.add(arch);
    const dome = new THREE.Mesh(new THREE.SphereGeometry(2.15, 16, 9, 0, Math.PI * 2, 0, Math.PI / 2), roof);
    dome.position.set(0, 8.55, -0.8);
    compound.add(dome);
    const tower = new THREE.Mesh(new THREE.BoxGeometry(2.2, 4.5, 2.2), trim);
    tower.position.set(4.1, 10.4, 3.8);
    const towerCap = new THREE.Mesh(new THREE.ConeGeometry(1.35, 1.8, 8), roof);
    towerCap.position.set(4.1, 13.55, 3.8);
    const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.22, 1.55, 0.22), dark);
    crossV.position.set(4.1, 15.15, 3.8);
    const crossH = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.22, 0.22), dark);
    crossH.position.set(4.1, 15.35, 3.8);
    compound.add(tower, towerCap, crossV, crossH);
    const signMap = shopTex("كنيسة مارمينا", "والقديس أغسطينوس", "#6b4b36", "#ffffff");
    if (signMap) {
      const sign = new THREE.Mesh(new THREE.PlaneGeometry(8.5, 1.6), new THREE.MeshStandardMaterial({ map: signMap, side: THREE.DoubleSide }));
      sign.position.set(0, 6.65, 6.72);
      compound.add(sign);
    }
    scene.add(compound);
  }

  // Palm-lined frontage around the six-school complex, matching the documented planting.
  {
    const p = spot(track.stops[5].s, 17.2);
    const group = new THREE.Group();
    group.position.set(p.x, 0, p.z);
    group.rotation.y = p.yaw;
    const trunkMat = new THREE.MeshStandardMaterial({ color: "#765332", roughness: 0.92 });
    const leafMat = new THREE.MeshStandardMaterial({ color: "#2f673c", roughness: 0.82 });
    for (let i = 0; i < 7; i++) {
      const x = -18 + i * 6;
      const h = 4.4 + (i % 3) * 0.35;
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.27, h, 7), trunkMat);
      trunk.position.set(x, h / 2, 0);
      group.add(trunk);
      for (let f = 0; f < 7; f++) {
        const leaf = new THREE.Mesh(new THREE.ConeGeometry(0.16, 3.2, 5), leafMat);
        const angle = (f / 7) * Math.PI * 2;
        leaf.position.set(x + Math.cos(angle) * 1.25, h + 0.45, Math.sin(angle) * 1.25);
        leaf.rotation.z = Math.cos(angle) * 0.72;
        leaf.rotation.x = Math.sin(angle) * 0.72;
        group.add(leaf);
      }
    }
    scene.add(group);
  }
"""
marker = "\n  const bumpMat = new THREE.MeshStandardMaterial({ map: bumpTexture() ?? undefined, roughness: 0.55 });"
if s.count(marker) != 1:
    raise SystemExit("fayoum.ts: church insertion marker not unique")
s = s.replace(marker, "\n" + church + marker, 1)
p.write_text(s, encoding="utf-8")

# Add a busier school-gate crowd to the otherwise evenly distributed pedestrians.
p = root / "src/game/fayoum.ts"
s = p.read_text(encoding="utf-8")
end = s.rfind("\n}")
if end < 0:
    raise SystemExit("fayoum.ts: placePeople function end not found")
crowd = """
  // Extra parent/student groups at the school exits during the daytime route.
  for (let j = 0; j < 28; j++) {
    const stop = track.stops[j % 2 === 0 ? 5 : 6];
    const sm = track.sample(stop.s + ((j % 7) - 3) * 2.1);
    const side = j % 2 === 0 ? 1 : -1;
    const rx = Math.cos(sm.yaw);
    const rz = -Math.sin(sm.yaw);
    const h = Math.abs(Math.sin(j * 8.31) * 43758.5453) % 1;
    const person = new THREE.Group();
    person.position.set(sm.x + rx * side * (ROAD_HALF + 3.1 + (j % 3) * 0.65), 0, sm.z + rz * side * (ROAD_HALF + 3.1 + (j % 3) * 0.65));
    person.rotation.y = sm.yaw + (side > 0 ? Math.PI : 0) + (h - 0.5) * 0.8;
    const scale = j % 4 === 0 ? 0.72 : 0.92 + h * 0.12;
    person.scale.setScalar(scale);
    const torso = new THREE.Mesh(bodyGeo, shirts[(j + 3) % shirts.length]);
    torso.position.y = 1.02;
    const head = new THREE.Mesh(headGeo, skins[(j + 2) % skins.length]);
    head.position.y = 1.48;
    const legL = new THREE.Mesh(legGeo, pants[j % pants.length]);
    legL.position.set(-0.09, 0.38, 0.04);
    const legR = new THREE.Mesh(legGeo, pants[(j + 1) % pants.length]);
    legR.position.set(0.09, 0.38, -0.04);
    const armL = new THREE.Mesh(armGeo, shirts[(j + 3) % shirts.length]);
    armL.position.set(-0.26, 1.05, 0);
    armL.rotation.z = 0.28;
    const armR = new THREE.Mesh(armGeo, shirts[(j + 3) % shirts.length]);
    armR.position.set(0.26, 1.05, 0);
    armR.rotation.z = -0.28;
    person.add(torso, head, legL, legR, armL, armR);
    scene.add(person);
  }
"""
s = s[:end] + "\n" + crowd + s[end:]
p.write_text(s, encoding="utf-8")


print("Applied Fayoum Street corridor and visual frontage changes.")
