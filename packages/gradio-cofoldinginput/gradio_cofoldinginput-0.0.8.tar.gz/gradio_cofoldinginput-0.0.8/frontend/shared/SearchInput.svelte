<script>
  import { createEventDispatcher } from "svelte";

  // import "../style.css";

  const dispatch = createEventDispatcher();

  export let database = "rcsb-bioass";
  export let index = 0;
  let databases = {
    "rcsb-3ligand": "CCD",
    pubchem: "Pubchem",
    "rcsb-bioass": "RCSB BioAssembly",
  };

  let placeholder = {
    "rcsb-3ligand": "e.g HEM, ZN, K, GOL ...",
    pubchem: "molecule name",
    "rcsb-bioass": "4 Letter PDB Code",
  };

  let currentSel = database;
  let searchInput = "";

  function triggerFetch() {
    dispatch("triggerFetch", {
      text: searchInput,
      database: currentSel,
      index: index,
    });
  }
</script>

<form class="max-w-lg mx-auto mb-2 my-2">
  <div class="flex">
    <label
      for="search-dropdown"
      class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
      >Search</label
    >
    <button
      id="dropdown-button"
      data-dropdown-toggle="dropdown"
      class="flex-shrink-0 z-10 inline-flex items-center py-2.5 px-4 text-sm font-medium text-center text-gray-900 bg-gray-100 border border-gray-300 rounded-s-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600"
      type="button"
      >{databases[currentSel]}
      <!-- <svg
        class="w-2.5 h-2.5 ms-2.5"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 10 6"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="m1 1 4 4 4-4"
        />
      </svg> -->
    </button>
    <div
      id="dropdown"
      class="z-10 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700"
    >
      <ul
        class="py-2 text-sm text-gray-700 dark:text-gray-200"
        aria-labelledby="dropdown-button"
      >
        <li>
          <button
            type="button"
            class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
            >Pubchem</button
          >
        </li>
        <li>
          <button
            type="button"
            class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
            >RCSB 3 Letter code</button
          >
        </li>
      </ul>
    </div>
    <div class="relative w-full">
      <input
        type="search"
        id="search-dropdown"
        class=" p-2.5 w-full h-full z-20 text-sm text-gray-900 bg-gray-50 rounded-e-lg border-s-gray-50 border-s-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-s-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500"
        style="display:block"
        placeholder={placeholder[currentSel]}
        on:input={(e) => (searchInput = e.target.value)}
      />
      <button
        type="submit"
        class="absolute top-0 end-0 p-2.5 text-sm font-medium h-full text-white bg-blue-700 rounded-e-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        on:click|preventDefault={triggerFetch}
      >
        <svg
          class="w-4 h-4"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 20 20"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
        <span class="sr-only">Search</span>
      </button>
    </div>
  </div>
</form>
