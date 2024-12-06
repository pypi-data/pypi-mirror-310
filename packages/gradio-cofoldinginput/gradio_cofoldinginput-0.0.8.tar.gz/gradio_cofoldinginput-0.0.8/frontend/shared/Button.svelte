<script>
  import { createEventDispatcher } from "svelte";

  // import "../style.css";

  const dispatch = createEventDispatcher();
  export let vals = [];
  function addNewChain(type) {
    dispatch("addNewChain", {
      type: type,
    });
  }
  function addCovalentModification() {
    dispatch("addCovalentModification");
  }

  let displayCovMod = false;
  // check if vals contains at least one protein and one ligand with sdf set
  $: {
    displayCovMod =
      vals.filter((val) => val.class === "protein" && val.sequence.length > 0)
        .length > 0 &&
      vals.filter((val) => val.class === "ligand" && val.sdf != "").length > 0;
  }
</script>

<div>
  <div class="flex justify-center mt-2 gap-2">
    <button
      class="flex items-center space-x-1 px-2 py-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
      on:click={() => {
        addNewChain("protein");
      }}
    >
      <svg
        data-slot="icon"
        fill="none"
        stroke-width="1.5"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
        class="w-4 h-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
        ></path>
      </svg>

      <span> Protein</span></button
    >

    <button
      class="flex items-center space-x-1 px-2 py-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
      on:click={() => {
        addNewChain("DNA");
      }}
    >
      <svg
        data-slot="icon"
        fill="none"
        stroke-width="1.5"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
        class="w-4 h-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
        ></path>
      </svg>

      <span> Nucleic acid</span></button
    >

    <button
      class="flex items-center space-x-1 px-2 py-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
      on:click={() => {
        addNewChain("ligand");
      }}
    >
      <svg
        data-slot="icon"
        fill="none"
        stroke-width="1.5"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
        class="w-4 h-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
        ></path>
      </svg>

      <span> Small molecule</span></button
    >

    {#if displayCovMod}
      <button
        class="flex items-center space-x-2 block rounded-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
        on:click={() => {
          addCovalentModification();
        }}
      >
        <svg
          data-slot="icon"
          fill="none"
          stroke-width="1.5"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
          class="w-4 h-4"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
          ></path>
        </svg>

        <span> Covalent modifcation</span></button
      >
    {/if}
  </div>
</div>
