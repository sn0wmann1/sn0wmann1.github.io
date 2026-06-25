export const ASCII_LOGO = `
    ███████╗███╗   ██╗ ██████╗ ██╗    ██╗
    ██╔════╝████╗  ██║██╔═══██╗██║    ██║
    ███████╗██╔██╗ ██║██║   ██║██║ █╗ ██║
    ╚════██║██║╚██╗██║██║   ██║██║███╗██║
    ███████║██║ ╚████║╚██████╔╝╚███╔███╔╝
    ╚══════╝╚═╝  ╚═══╝ ╚═════╝  ╚══╝ ╚══╝
`

export const COMMIT_LOG = [
  { hash: '1eac8d5', date: '2026-06-25', msg: 'feat (scripts): update publish-public.sh' },
  { hash: 'dedf42d', date: '2026-06-25', msg: 'chore: add 2 configs, 2 files' },
  { hash: 'f1b4c2d', date: '2026-06-25', msg: 'refactor (scripts): rename 3 files; add 8 scripts, 1 qml, 1 config, 1 doc, 1 file; update config.json; remove MEMORY.md' },
  { hash: '72b5e95', date: '2026-06-22', msg: 'docs (docs): update, 12 files' },
  { hash: 'a0c3f7e', date: '2026-06-18', msg: 'fix: rgb-related QML files' },
  { hash: 'd4e5f6a', date: '2026-06-15', msg: 'feat: add lock screen breathing clock, weather particles' },
  { hash: 'b2c3d4e', date: '2026-06-10', msg: 'fix: husky pre-commit space handling' },
  { hash: '9a8b7c6', date: '2026-06-05', msg: 'refactor: migrate docs to Freezer PC dir' },
  { hash: '7f6e5d4', date: '2026-05-30', msg: 'feat: remote control setup, OC pilot' },
  { hash: '3a4b5c6', date: '2026-05-24', msg: 'feat: fastfetch, subagents, root cleanup' },
]

export interface Project {
  name: string; url: string; desc: string; lang: string
}

export const PROJECTS: Project[] = [
  { name: 'snowdots', url: 'https://github.com/sn0wmann1/snowdots', desc: 'dotfiles — Hyprland rice, matugen M3, Caelestia QML', lang: 'QML/Shell' },
  { name: 'clapfinder', url: 'https://github.com/sn0wmann1/ClapFinder', desc: 'detect claps via mic, trigger actions', lang: 'Python' },
  { name: 'commit-message-skill', url: 'https://github.com/sn0wmann1/commit-message-skill', desc: 'conventional commit CLI with heuristics', lang: 'Node.js' },
  { name: 'archinstall-personal', url: 'https://github.com/sn0wmann1/archinstall-personal', desc: 'Arch Linux installer (LUKS+BTRFS)', lang: 'Shell' },
  { name: 'mad68-custom-animation', url: 'https://github.com/sn0wmann1/MAD-68-custom-animation', desc: 'custom animations for MAD68 HE keyboard', lang: 'Python' },
]

export const SKILLS: Record<string, string[]> = {
  'development': ['Python', 'QML', 'Shell', 'TypeScript', 'HTML/CSS', 'JavaScript'],
  'config/rice': ['Hyprland', 'Caelestia', 'matugen', 'OpenRGB', 'systemd', 'fish', 'kitty'],
  'infrastructure': ['Arch Linux', 'Docker', 'self-host', 'GH Actions', 'Tailscale', 'Nginx'],
}

export const HOBBIES = [
  { icon: '🐧', name: 'Linux', desc: 'ricing, dotfiles, custom configs' },
  { icon: '🖥', name: 'Homelab', desc: 'self-hosting, servers, networking' },
  { icon: '🎮', name: 'Gaming', desc: 'custom RGB, keybinds, setups' },
  { icon: '⌨', name: 'Keyboards', desc: 'MAD68 HE, modding, firmware' },
]

export type Line = { text: string; html?: string; raw?: string }

const TYPED = [
  '    OS:        Arch Linux x86_64',
  '    WM:        Hyprland',
  '    Shell:     fish 4.0',
  '    Terminal:  kitty',
  '    Colors:    matugen Material You',
  '    Keyboard:  MAD68 HE',
  '    Status:    active_and_coding',
]

const ABOUT = [
  'IT graduate. Linux tinkerer, homelab enthusiast, keyboard modder.',
  'I build things — dotfiles, color pipelines, custom RGB controllers.',
  'Writing about it at the blog.',
  '',
  '  Principles:',
  '    • Open source, always',
  '    • Form follows function',
  '    • Automation over repetition',
]

const TRAIN = [
  '    ====        ________                ___________',
  ' _D _|  |_______/        \\__I_I_____===__|_________|',
  '  |(_)---  |   H\\________/ |   |        =|___ ___|',
  '  /     |  |   H  |  |     |   |         ||_| |_||',
  '  |      |  |   H  |__--------------------| [___] |',
  '  | ________|___H__/__|_____/[][]~_______|       |',
  '  |/ |   |-----------I_____I [][] []  D   |=======|',
  '  __/ =| o |=-~~\\\\  /~~\\\\  /~~\\\\  /~~\\\\ ____Y___________',
  '  |/-=|___|= O=====O=====O=====O  |_________________|',
  '   \\_/      \\__/  \\__/  \\__/  \\__/',
]

export const COMMANDS: Record<string, () => Line[]> = {
  help: () => [
    { text: 'Available commands:' },
    { text: '' },
    { text: '  help      Show this help menu' },
    { text: '  neofetch  Display system info' },
    { text: '  about     Read about me' },
    { text: '  projects  List my projects' },
    { text: '  skills    Tools and technologies' },
    { text: '  hobbies   What I do when not coding' },
    { text: '  log       Recent commit history' },
    { text: '  theme     Toggle light/dark mode' },
    { text: '  matrix    Toggle green rain' },
    { text: '  train     🚂' },
    { text: '  clear     Clear terminal' },
  ],

  neofetch: () => [
    { text: '' },
    ...ASCII_LOGO.split('\n').map(l => ({ text: l })),
    { text: '' },
    { text: '  snow@sn0wmann1' },
    { text: '  ---------------' },
    ...TYPED.map(t => ({ text: t })),
    { text: '' },
  ],

  about: () => [
    { text: '' },
    ...ABOUT.map(t => ({ text: t })),
    { text: '' },
  ],

  projects: () => [
    { text: '' },
    ...PROJECTS.map(p =>
      ({ html: `  <span style="color:#2563eb">◆</span> <a href="${p.url}" style="color:#d4d4d8;text-decoration:none">${p.name}</a> <span style="color:#3f3f52">—</span> <span style="color:#5c5c72">${p.desc}</span> <span style="color:#3f3f52;font-size:12px">${p.lang}</span>` })
    ),
    { text: '' },
  ],

  skills: () => {
    const lines: Line[] = [{ text: '' }]
    for (const [cat, items] of Object.entries(SKILLS)) {
      lines.push({ html: `  <span style="color:#2563eb">$ ${cat}</span>` })
      lines.push({ text: `    ${items.join(', ')}` })
      lines.push({ text: '' })
    }
    return lines
  },

  hobbies: () => [
    { text: '' },
    ...HOBBIES.map(h =>
      ({ text: `  ${h.icon}  ${h.name} — ${h.desc}` })
    ),
    { text: '' },
  ],

  log: () => [
    { text: '' },
    ...COMMIT_LOG.map(c =>
      ({ html: `  <span style="color:#3f3f52">${c.date}</span> <span style="color:#2563eb">${c.hash.slice(0,7)}</span> ${c.msg}` })
    ),
    { text: '' },
  ],

  train: () => [
    { text: '' },
    ...TRAIN.map(l => ({ text: l })),
    { text: '' },
  ],

  'sudo rm': () => [
    { text: '' },
    { text: '  😈 nice try' },
    { text: '' },
  ],
}

export const FALLBACK = (cmd: string): Line[] => [
  { text: `  bash: ${cmd}: command not found. Try 'help'.` },
]

export function getOutput(input: string): Line[] {
  const trimmed = input.trim().toLowerCase()
  if (trimmed === '') return []
  if (trimmed === 'clear') return [{ text: '__CLEAR__' }]
  if (trimmed === 'matrix') return [{ text: '__MATRIX__' }]
  if (trimmed === 'theme') return [{ text: '__THEME__' }]
  if (trimmed === 'sudo rm -rf /' || trimmed === 'sudo rm -rf /*') return COMMANDS['sudo rm']()
  if (trimmed.startsWith('sudo rm')) return COMMANDS['sudo rm']()
  const fn = COMMANDS[trimmed]
  if (fn) return fn()
  return FALLBACK(trimmed)
}
