// Clés de licence Taverne Voice : même format que licence.go dans le logiciel.
//
//   [0] version = 1   [1] type (1 = complète)   [2:6] numéro
//   [6:8] émise le (jours depuis le 1er janvier 2026)
//   [8:10] expire le (idem, 0 = jamais)   [10] longueur du nom   [11:11+n] nom (UTF-8)
//   puis 64 octets de signature Ed25519 de tout ce qui précède.
// Encodage : base32 Crockford, groupes de 5, préfixe « TV1- ».

import * as ed from "./ed25519.js";

const ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
const ORIGINE = Date.UTC(2026, 0, 1);
const JOUR = 86400000;
export const NOM_MAX = 30; // octets

export function encoderBase32(octets) {
  let sortie = "", acc = 0, bits = 0;
  for (const x of octets) {
    acc = ((acc << 8) | x) & 0xffff;
    bits += 8;
    while (bits >= 5) { bits -= 5; sortie += ALPHABET[(acc >> bits) & 31]; }
  }
  if (bits > 0) sortie += ALPHABET[(acc << (5 - bits)) & 31];
  return sortie;
}

export function decoderBase32(texte) {
  const sortie = [];
  let acc = 0, bits = 0;
  for (let c of texte) {
    if (c === "O") c = "0";
    if (c === "I" || c === "L") c = "1";
    const v = ALPHABET.indexOf(c);
    if (v < 0) throw new Error(`caractère « ${c} » inattendu`);
    acc = ((acc << 5) | v) & 0xffff;
    bits += 5;
    if (bits >= 8) { bits -= 8; sortie.push((acc >> bits) & 255); }
  }
  return Uint8Array.from(sortie);
}

export function normaliser(texte) {
  let t = String(texte).toUpperCase().trim();
  if (t.startsWith("TV1-")) t = t.slice(4);
  else if (t.startsWith("TV1")) t = t.slice(3);
  return t.replace(/[\s-]/g, "");
}

export function formater(octets) {
  return "TV1-" + encoderBase32(octets).match(/.{1,5}/g).join("-");
}

export const jourDe = (date) => Math.floor((Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) - ORIGINE) / JOUR);
export const dateDuJour = (j) => new Date(ORIGINE + j * JOUR);

// coupe le nom à NOM_MAX octets sans casser un caractère
export function couperNom(nom) {
  const enc = new TextEncoder();
  let n = String(nom || "").trim();
  while (enc.encode(n).length > NOM_MAX) n = [...n].slice(0, -1).join("");
  return n.trim();
}

export function numeroAleatoire() {
  const b = new Uint8Array(4);
  crypto.getRandomValues(b);
  return b;
}

export const hex = (b) => [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
const deHex = (h) => Uint8Array.from(h.match(/../g).map((x) => parseInt(x, 16)));
const enBase64 = (b) => btoa(String.fromCharCode(...b));
const deBase64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

/** Crée une clé signée. graine : les 32 octets de la clé privée. */
export async function creerCle(graine, { numero = numeroAleatoire(), nom = "", emise, expire = 0 } = {}) {
  const nomOctets = new TextEncoder().encode(couperNom(nom));
  const corps = new Uint8Array(11 + nomOctets.length);
  corps[0] = 1;
  corps[1] = 1;
  corps.set(typeof numero === "string" ? deHex(numero) : numero, 2);
  const e = emise ?? jourDe(new Date());
  corps[6] = e >> 8; corps[7] = e & 255;
  corps[8] = expire >> 8; corps[9] = expire & 255;
  corps[10] = nomOctets.length;
  corps.set(nomOctets, 11);
  const signature = await ed.signAsync(corps, graine);
  const tout = new Uint8Array(corps.length + 64);
  tout.set(corps);
  tout.set(signature, corps.length);
  return { cle: formater(tout), numero: hex(corps.subarray(2, 6)).toUpperCase(), nom: new TextDecoder().decode(nomOctets), emise: e, expire };
}

/** Lit une clé et vérifie sa signature avec la clé publique. */
export async function lireCle(texte, publique) {
  let b;
  try { b = decoderBase32(normaliser(texte)); } catch (e) { return { valide: false, raison: "La clé contient des caractères inattendus." }; }
  if (b.length < 75) return { valide: false, raison: "La clé est incomplète." };
  const n = b[10];
  if (b.length < 11 + n + 64) return { valide: false, raison: "La clé est incomplète." };
  const corps = b.subarray(0, 11 + n);
  const sig = b.subarray(11 + n, 11 + n + 64);
  const info = {
    numero: hex(corps.subarray(2, 6)).toUpperCase(),
    nom: new TextDecoder().decode(corps.subarray(11)),
    emise: (corps[6] << 8) | corps[7],
    expire: (corps[8] << 8) | corps[9],
  };
  const ok = corps[0] === 1 && (await ed.verifyAsync(sig, corps, publique));
  return ok ? { valide: true, ...info } : { valide: false, raison: "La signature ne correspond pas : cette clé n'a pas été créée avec ta clé de créateur.", ...info };
}

// ---------------------------------------------------------------- clé de créateur chiffrée

async function deriver(mdp, sel, iterations) {
  const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(mdp), "PBKDF2", false, ["deriveKey"]);
  return crypto.subtle.deriveKey({ name: "PBKDF2", hash: "SHA-256", salt: sel, iterations }, base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
}

/** Déchiffre la clé privée avec le mot de passe. Lance une erreur si le mot de passe est faux. */
export async function dechiffrerGraine(fichier, mdp) {
  const cle = await deriver(mdp, deBase64(fichier.sel), fichier.iterations);
  let graine;
  try {
    graine = new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: deBase64(fichier.iv) }, cle, deBase64(fichier.donnees)));
  } catch (e) {
    throw new Error("Mot de passe incorrect.");
  }
  const publique = await ed.getPublicKeyAsync(graine);
  if (enBase64(publique) !== fichier.publique) throw new Error("Le fichier de la clé de créateur est abîmé.");
  return { graine, publique };
}

/** Rechiffre la clé privée avec un nouveau mot de passe (pour changer de mot de passe). */
export async function chiffrerGraine(graine, mdp, iterations = 600000) {
  const sel = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const cle = await deriver(mdp, sel, iterations);
  const donnees = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cle, graine));
  const publique = await ed.getPublicKeyAsync(graine);
  return { version: 1, algo: "PBKDF2-SHA256/AES-256-GCM/Ed25519", iterations, sel: enBase64(sel), iv: enBase64(iv), donnees: enBase64(donnees), publique: enBase64(publique) };
}

export const clePublique = (fichier) => deBase64(fichier.publique);
