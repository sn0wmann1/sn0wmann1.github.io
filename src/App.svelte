<script lang="ts">
  import { tick } from 'svelte'
  import MatrixRain from './lib/MatrixRain.svelte'
  import Train from './lib/Train.svelte'
  import { ASCII_LOGO, getOutput, type Line } from './lib/commands'

  type Entry = { type: 'input' | 'output'; content: Line[]; text?: string }

  let history = $state<Entry[]>([])
  let currentInput = $state('')
  let matrixActive = $state(false)
  let trainActive = $state(false)
  let inputEl: HTMLInputElement
  let terminalEnd: HTMLDivElement

  history = [
    { type: 'output', content: ASCII_LOGO.split('\n').map(l => ({ text: l })) },
    { type: 'output', content: [{ text: '' }, { text: '  Welcome to my portfolio. Type help for available commands.' }, { text: '' }] },
  ]

  function handleKey(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault()
      const cmd = currentInput.trim()
      history = [...history, { type: 'input', text: currentInput, content: [] }]
      currentInput = ''

      if (cmd.toLowerCase() === 'clear') {
        history = []
      } else if (cmd.toLowerCase() === 'matrix') {
        matrixActive = !matrixActive
        history = [...history, { type: 'output', content: [{ text: matrixActive ? '  matrix rain: on' : '  matrix rain: off' }] }]
      } else if (cmd.toLowerCase() === 'theme') {
        const root = document.documentElement
        const isDark = root.style.getPropertyValue('--bg') === '#000000' || !root.style.getPropertyValue('--bg')
        root.style.setProperty('--bg', isDark ? '#f5f5f0' : '#000000')
        root.style.setProperty('--text', isDark ? '#1a1a1a' : '#e0e0e0')
        root.style.setProperty('--muted', isDark ? '#888888' : '#555555')
        root.style.setProperty('--border', isDark ? '#d0d0c8' : '#1a1a1a')
        history = [...history, { type: 'output', content: [{ text: `  theme: ${isDark ? 'light' : 'dark'}` }] }]
      } else if (cmd.toLowerCase() === 'train' || cmd.toLowerCase() === 'sl') {
        trainActive = true
        history = [...history, { type: 'output', content: [{ text: '' }, ...getOutput('train'), { text: '' }] }]
        setTimeout(() => { trainActive = false }, 4000)
      } else {
        const output = getOutput(cmd)
        if (output.length > 0) {
          history = [...history, { type: 'output', content: output }]
        }
      }

      tick().then(() => {
        terminalEnd?.scrollIntoView({ behavior: 'smooth' })
        inputEl?.focus()
      })
    }
  }

  function handleClick() {
    inputEl?.focus()
  }
</script>

<svelte:head>
  <title>snow — ~</title>
</svelte:head>

<MatrixRain active={matrixActive} />
<Train active={trainActive} />

<div class="terminal" role="application" onclick={handleClick}>
  <div class="titlebar">
    <div class="dots">
      <span class="dot r"></span>
      <span class="dot y"></span>
      <span class="dot g"></span>
    </div>
    <span class="title">snow@portfolio:~</span>
  </div>

  <div class="screen">
    {#each history as entry}
      {#if entry.type === 'input'}
        <div class="line input-line">
          <span class="prompt-user">guest</span><span class="prompt-at">@</span><span class="prompt-host">snow</span>
          <span class="prompt-sep">:</span><span class="prompt-path">~</span><span class="prompt-dollar">$</span>
          <span class="input-text">{entry.text}</span>
        </div>
      {:else}
        {#each entry.content as line}
          <div class="line output-line">
            {#if line.html}
              {@html line.html}
            {:else}
              <span class="output-text" class:error={line.text.includes('command not found')}>
                {line.text}
              </span>
            {/if}
          </div>
        {/each}
      {/if}
    {/each}

    <div class="line input-line prompt-line">
      <span class="prompt-user">guest</span><span class="prompt-at">@</span><span class="prompt-host">snow</span>
      <span class="prompt-sep">:</span><span class="prompt-path">~</span><span class="prompt-dollar">$</span>
      <input
        bind:this={inputEl}
        bind:value={currentInput}
        onkeydown={handleKey}
        spellcheck="false"
        autocomplete="off"
        autofocus
      />
      <span class="cursor">▊</span>
    </div>
    <div bind:this={terminalEnd}></div>
  </div>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  :global(html), :global(body) {
    height: 100%;
  }
  :global(body) {
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    background: #000000;
    color: #e0e0e0;
    font-size: 15px;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  :global(#app) {
    height: 100%;
  }
  :global(:root) {
    --bg: #000000;
    --text: #e0e0e0;
    --muted: #555555;
    --border: #1a1a1a;
    --accent: #2563eb;
  }
  :global(::selection) {
    background: #2563eb44;
    color: #e0e0e0;
  }

  .terminal {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    z-index: 1;
  }
  .titlebar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-bottom: 1px solid var(--border);
    user-select: none;
    flex-shrink: 0;
  }
  .dots {
    display: flex;
    gap: 6px;
  }
  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .dot.r { background: #ff5f56; }
  .dot.y { background: #ffbd2e; }
  .dot.g { background: #27c93f; }
  .title {
    font-size: 13px;
    color: var(--muted);
    margin-left: 8px;
    flex: 1;
  }
  .screen {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .line {
    font-size: 15px;
    line-height: 1.7;
  }
  .input-line {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    margin-bottom: 2px;
  }
  .output-line {
    padding: 0;
    margin-bottom: 0;
  }
  .output-text { white-space: pre-wrap; word-break: break-word; }
  .output-text.error { color: #ff4444; }

  .prompt-user { color: #2563eb; }
  .prompt-at { color: var(--muted); }
  .prompt-host { color: #2563eb; }
  .prompt-sep { color: var(--muted); }
  .prompt-path { color: #3b82f6; }
  .prompt-dollar { color: #888888; }
  .input-text { color: var(--text); margin-left: 2px; }

  .prompt-line input {
    flex: 1;
    min-width: 80px;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font: inherit;
    font-size: 15px;
    caret-color: transparent;
    margin-left: 0;
  }
  .cursor {
    animation: blink 1s step-end infinite;
    color: #e0e0e0;
    font-size: 15px;
    margin-left: -1px;
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }

  @media (max-width: 600px) {
    .screen { padding: 16px; }
    .line, .prompt-line input, .title { font-size: 13px; }
  }
</style>
