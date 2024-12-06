<script>
  export let seq = "";

  // convert sequence into chunked array of 10

  let chunked_seq = seq.match(/.{1,10}/g);

  if (chunked_seq == null) {
    chunked_seq = [];
  }
  // store residue index of each residue per chunk
  let chunk_ids = chunked_seq.map((chunk, i) => {
    return chunk.split("").map((_, j) => {
      return i * 10 + j + 1;
    });
  });
</script>

<div class="sequence_container text-xs">
  {#each chunked_seq as chunk, i}
    <div class="sequence__chunk">
      {#each chunk as letter, j}
        <span
          class="p-0.1 text-center w-full inline hover:font-bold cursor-pointer item-selectable ds-selectable"
          style="font-family: monospace;"
        >
          <div class="inline-block p-0.5" title="residue {chunk_ids[i][j]}">
            {letter}
          </div>
        </span>
      {/each}
    </div>
  {/each}
</div>

<style>
  .sequence_container {
    overflow-wrap: anywhere;
    counter-reset: sequence;
  }

  .sequence_container .sequence__chunk {
    display: inline-block;
    margin: 0.1rem 0 1rem 1rem;
    /* width: 10ch; */
    position: relative;
    white-space: nowrap;
  }

  .sequence_container .sequence__chunk:not(:last-child):before,
  .sequence_container .sequence__chunk--display-last:before {
    content: counter(sequence);
    counter-increment: sequence 10;
    position: absolute;
    top: -0.8em;
    right: 0;
    opacity: 0.5;
    font-weight: bold;
  }

  .sequence-container .sequence__chunk::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transform-origin: left;
    transform: scaleX(0.1);
    box-shadow: var(--box-shadow);
  }

  .sequence__chunk span {
    padding: 0 0.05rem;
  }
</style>
