<script lang="ts">
  import { onMount } from 'svelte'

  let container = $state<HTMLDivElement>()
  let offset = 0
  let animId: number

  let { active = false }: { active: boolean } = $props()

  onMount(() => {
    if (!active) return
    const frame = () => {
      offset = (offset + 1) % 80
      if (container) container.style.transform = `translateX(${offset}px)`
      animId = requestAnimationFrame(frame)
    }
    animId = requestAnimationFrame(frame)
    return () => cancelAnimationFrame(animId)
  })
</script>

{#if active}
  <div bind:this={container} style="
    position:fixed;bottom:20px;left:10%;z-index:5;pointer-events:none;
    font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.15;
    color:#d4d4d8;opacity:0.7;white-space:pre;
  ">
<pre>    ====        ________                ___________                    </pre>
<pre> _D _|  |_______/        \__I_I_____===__|_________|                  </pre>
<pre>  |(_)---  |   H\________/ |   |        =|___ ___|                    </pre>
<pre>  /     |  |   H  |  |     |   |         ||_| |_||                    </pre>
<pre>  |      |  |   H  |__--------------------| [___] |                   </pre>
<pre>  | ________|___H__/__|_____/[][]~_______|       |                   </pre>
<pre>  |/ |   |-----------I_____I [][] []  D   |=======|                   </pre>
<pre>  __/ =| o |=-~~  \/~~  \/~~  \/~~  ____Y___________                 </pre>
<pre>  |/-=|___|= O=====O=====O=====O  |_________________|                 </pre>
<pre>   \_/      \__/  \__/  \__/  \__/                                    </pre>
  </div>
{/if}
