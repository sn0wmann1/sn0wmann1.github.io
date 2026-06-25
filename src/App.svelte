<script lang="ts">
  import { tick, mount } from 'svelte'
  import MatrixRain from './lib/MatrixRain.svelte'
  import Train from './lib/Train.svelte'
  import { ASCII_LOGO, getOutput, type Line } from './lib/commands'

  let history = $state<{ type: 'input' | 'output'; content: Line[]; text?: string }[]>([])
  let currentInput = $state('')
  let matrixActive = $state(false)
  let trainActive = $state(false)
  let inputEl: HTMLInputElement
  let terminalEnd: HTMLDivElement
  let dark = $state(true)

  $effect(() => {
    document.documentElement.style.setProperty('--bg', dark ? '#0a0a0f' : '#f4f4f0')
    document.documentElement.style.setProperty('--text', dark ? '#d4d4d8' : '#1a1a1a')
    document.documentElement.style.setProperty('--muted', dark ? '#3f3f52' : '#8888a0')
  })

  history = [
    { type: 'output', content: ASCII_LOGO.split('\n').map(l => ({ text: l })) },
    { type: 'output', content: [{ text: '' }, { text: '  Welcome. Type help for available commands.' }, { text: '' }] },
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
        history = [...history, { type: 'output', content: [{ text: matrixActive ? '  Matrix rain: ON' : '  Matrix rain: OFF' }] }]
      } else if (cmd.toLowerCase() === 'theme') {
        dark = !dark
        history = [...history, { type: 'output', content: [{ text: `  Theme: ${dark ? 'dark' : 'light'}` }] }]
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

<div class="terminal" style="background:{dark?'var(--bg)':'var(--bg)'}" role="presentation" onclick={handleClick}>
  <div class="titlebar" style="border-color:{dark?'#1e1e2a':'#d4d4c8'};background:{dark?'#12121a':'#e8e8e0'}">
    <div class="dots">
      <span class="dot r"></span>
      <span class="dot y"></span>
      <span class="dot g"></span>
    </div>
    <span class="title" style="color:{dark?'#5c5c72':'#8888a0'}">snow@sn0wmann1.github.io — bash — 80×24</span>
  </div>

  <div class="screen" style="color:var(--text)">
    {#each history as entry}
      {#if entry.type === 'input'}
        <div class="line input-line" style="color:#2563eb">
          <span style="color:#2563eb">guest@snow</span><span style="color:#5c5c72">:</span><span style="color:#3b82f6">~</span><span style="color:#a1a1aa">$</span> {entry.text}
        </div>
      {:else}
        {#each entry.content as line}
          {#if line.html}
            <div class="line output-line" style="color:var(--text)">{@html line.html}</div>
          {:else}
            <div class="line output-line" style="color:{line.text.includes('command not found')?'#ff5f56':'var(--text)'}">{line.text}</div>
          {/if}
        {/each}
      {/if}
    {/each}

    <div class="line input-line prompt" style="color:#2563eb">
      <span style="color:#2563eb">guest@snow</span><span style="color:#5c5c72">:</span><span style="color:#3b82f6">~</span><span style="color:#a1a1aa">$</span>
      <input
        bind:this={inputEl}
        bind:value={currentInput}
        onkeydown={handleKey}
        spellcheck="false"
        autocomplete="off"
        autofocus
      />
      <span class="cursor">█</span>
    </div>
    <div bind:this={terminalEnd}></div>
  </div>
</div>

<style>
  .terminal {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    z-index: 1;
  }
  :global(:root) {
    --bg: #0a0a0f;
    --text: #d4d4d8;
    --muted: #3f3f52;
  }
  .titlebar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-bottom: 1px solid;
    user-select: none;
    flex-shrink: 0;
  }
  .dots { display: flex; gap: 6px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot.r { background: #ff5f56; }
  .dot.y { background: #ffbd2e; }
  .dot.g { background: #27c93f; }
  .title { font-size: 12px; margin-left: 12px; flex: 1; }
  .screen {
    flex: 1;
    padding: 20px 24px;
    overflow-y: auto;
  }
  .line {
    font-size: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .output-line { padding: 0; }
  .input-line {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
  }
  .prompt input {
    flex: 1;
    min-width: 100px;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font: inherit;
    font-size: 14px;
    caret-color: transparent;
  }
  .cursor {
    animation: blink 1s step-end infinite;
    color: #d4d4d8;
  }
  @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
  @media (max-width: 600px) {
    .screen { padding: 12px 14px; }
    .line, .prompt input { font-size: 12px; }
  }
</style>
