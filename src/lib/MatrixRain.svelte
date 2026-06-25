<script lang="ts">
  import { onMount } from 'svelte'

  let canvas = $state<HTMLCanvasElement>()
  let animId: number

  let { active = false }: { active: boolean } = $props()

  onMount(() => {
    if (!canvas || !active) return
    const ctx = canvas.getContext('2d')!
    let w: number, h: number
    const resize = () => { w = canvas.width = innerWidth; h = canvas.height = innerHeight }
    resize()
    addEventListener('resize', resize)

    const cols = Math.floor(w / 14)
    const drops: number[] = Array(cols).fill(0).map(() => Math.random() * -100)
    const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789'

    function draw() {
      ctx.fillStyle = 'rgba(10, 10, 15, 0.05)'
      ctx.fillRect(0, 0, w, h)
      ctx.font = '14px JetBrains Mono, monospace'

      for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)]
        const x = i * 14
        const y = drops[i] * 14
        ctx.fillStyle = y > 0 && Math.random() > 0.98 ? '#00ff41' : '#00ff4166'
        ctx.fillText(text, x, y)
        if (drops[i] * 14 > h && Math.random() > 0.975) drops[i] = 0
        drops[i]++
      }
      animId = requestAnimationFrame(draw)
    }
    draw()

    return () => cancelAnimationFrame(animId)
  })
</script>

{#if active}
  <canvas bind:this={canvas} style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none"></canvas>
{/if}
