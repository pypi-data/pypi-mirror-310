<script>
  import { createEventDispatcher } from "svelte";

  import Sequence from "./Sequence.svelte";
  import SearchInput from "./SearchInput.svelte";
  import Molecule from "./Molecule.svelte";

  // import "../style.css";

  const dispatch = createEventDispatcher();

  export let vals = [];

  export let covMods = [];

  let showCovModVals = [];
  $: {
    if (covMods) {
      // iterate over each val
      showCovModVals = vals.map((val) => {
        // check if val is in covMods and return index in CovMods or null
        return covMods.findIndex((covMod) => covMod.ligand === val.chain);
        // if index is not -1 return true else false

        // return covMods.some((covMod) => covMod.ligand === val.chain);
      });

      // dispatch("updateCovMod", covMods);
    }
  }

  let labels = {
    DNA: "NA sequence",
    RNA: "NA sequence",
    protein: "Protein sequence",
    ligand: "Small molecule",
  };

  let colorCode = {
    DNA: "bg-green-200 text-blue-800",
    RNA: "bg-green-200 text-blue-800",
    protein: "bg-blue-200 text-blue-800",
    ligand: "bg-orange-200 text-blue-800",
  };

  let metals = [
    "ZN",
    "MG",
    "CA",
    "FE",
    "NA",
    "K",
    "CL",
    "CU",
    "MN",
    "CO",
    "NI",
  ];

  let proteinChains = [];

  $: proteinChains = vals
    .filter((val) => val.class === "protein")
    .map((val) => val.chain);

  let ligandChains = [];

  $: ligandChains = vals
    .filter((val) => val.class === "ligand")
    .map((val) => val.chain);

  let residue_atoms = {
    A: ["C", "CA", "CB", "N", "O"],
    R: ["C", "CA", "CB", "CG", "CD", "CZ", "N", "NE", "O", "NH1", "NH2"],
    D: ["C", "CA", "CB", "CG", "N", "O", "OD1", "OD2"],
    N: ["C", "CA", "CB", "CG", "N", "ND2", "O", "OD1"],
    C: ["C", "CA", "CB", "N", "O", "SG"],
    E: ["C", "CA", "CB", "CG", "CD", "N", "O", "OE1", "OE2"],
    N: ["C", "CA", "CB", "CG", "CD", "N", "NE2", "O", "OE1"],
    G: ["C", "CA", "N", "O"],
    H: ["C", "CA", "CB", "CG", "CD2", "CE1", "N", "ND1", "NE2", "O"],
    I: ["C", "CA", "CB", "CG1", "CG2", "CD1", "N", "O"],
    L: ["C", "CA", "CB", "CG", "CD1", "CD2", "N", "O"],
    K: ["C", "CA", "CB", "CG", "CD", "CE", "N", "NZ", "O"],
    M: ["C", "CA", "CB", "CG", "CE", "N", "O", "SD"],
    F: ["C", "CA", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ", "N", "O"],
    P: ["C", "CA", "CB", "CG", "CD", "N", "O"],
    S: ["C", "CA", "CB", "N", "O", "OG"],
    T: ["C", "CA", "CB", "CG2", "N", "O", "OG1"],
    W: [
      "C",
      "CA",
      "CB",
      "CG",
      "CD1",
      "CD2",
      "CE2",
      "CE3",
      "CZ2",
      "CZ3",
      "CH2",
      "N",
      "NE1",
      "O",
    ],
    Y: [
      "C",
      "CA",
      "CB",
      "CG",
      "CD1",
      "CD2",
      "CE1",
      "CE2",
      "CZ",
      "N",
      "O",
      "OH",
    ],
    V: ["C", "CA", "CB", "CG1", "CG2", "N", "O"],
  };

  let resmap = {
    H: "HIS",
    A: "ALA",
    R: "ARG",
    N: "ASN",
    D: "ASP",
    C: "CYS",
    E: "GLU",
    Q: "GLN",
    G: "GLY",
    H: "HIS",
    I: "ILE",
    L: "LEU",
    K: "LYS",
    M: "MET",
    F: "PHE",
    P: "PRO",
    S: "SER",
    T: "THR",
    W: "TRP",
    Y: "TYR",
    V: "VAL",
  };

  function getResAtoms(covMod) {
    // get sequence of matching protein chain
    let seq = vals.find((val) => val.chain === covMod.protein).sequence;

    //do something if sequence is too short
    if (seq.length < covMod.residue) {
      alert("Residue number is too high");
      return [];
    }
    // get residue
    let residue = seq[covMod.residue - 1];
    // get atoms
    return residue_atoms[residue];
  }

  function getResidues(covMod) {
    // get sequence of matching protein chain
    let seq = vals.find((val) => val.chain === covMod.protein).sequence;

    // map single letters to three letter residues
    return Array.from(seq).map((residue) => resmap[residue]);
  }

  function getResname(covMod) {
    // get sequence of matching protein chain
    let seq = vals.find((val) => val.chain === covMod.protein).sequence;
    // get residue
    let residue = seq[covMod.residue - 1];
    // get atoms
    return resmap[residue];
  }

  function updateMol(event) {
    let index = event.detail.index;
    covMods[index].mol = event.detail.mol;
    covMods[index].attachmentIndex = event.detail.attachmentIndex;
    covMods[index].deleteIndexes = event.detail.deleteIndexes;

    dispatch("updateCovMod", covMods);
  }

  function handleMessage(event) {
    // fetch sdf content from https://files.rcsb.org/ligands/download/{name}_ideal.sdf
    // alert(event.detail.text);

    fetch(
      `https://files.rcsb.org/ligands/download/${event.detail.text}_ideal.sdf`
    )
      .then((response) => {
        if (!response.ok) {
          // Check if the status code is 200
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((data) => {
        dispatch("updateVals", {
          sdf: data,
          name: event.detail.text,
          index: event.detail.index,
          close: true,
        });
      })
      .catch((error) => {
        alert("Error fetching sdf file");
      });
  }
</script>

<div data-accordion="collapse">
  {#each vals as item, i}
    <h2 id={`accordion-collapse-heading-${i}`}>
      <button
        type="button"
        class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-gray-200 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
        data-accordion-target={`#accordion-collapse-body-${i}`}
        class:rounded-t-xl={i === 0}
        class:border-b-0={i != vals.length - 1}
        aria-expanded={item.open}
        aria-controls={`accordion-collapse-body-${i}`}
        on:click={() => (item.open = !item.open)}
      >
        <div class="flex items-center justify-start">
          <span
            class="inline-flex items-center justify-center p-1 px-2 text-xs font-semibold rounded-full {colorCode[
              item.class
            ]}"
          >
            {item.chain}
          </span>
          <span class="p-1">{labels[item.class]}</span>
          {#if ["DNA", "RNA", "protein"].includes(item.class)}
            {#if item.msa}
              <span
                class=" ml-4 inline-flex items-center justify-center p-1 px-2 text-xs font-semibold rounded-full border border-gray-300"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-3 mr-1"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3.75 6.75h16.5M3.75 12H12m-8.25 5.25h16.5"
                  />
                </svg>

                MSA
              </span>
            {:else}
              <span
                class="inline-flex items-center justify-center p-1 px-2 text-xs font-semibold rounded-full border border-gray-300"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-3 mr-1"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M5 12h14"
                  />
                </svg>

                single sequence
              </span>
            {/if}
          {/if}

          <span class="px-2 text-gray-800 font-bold">
            {#if !item.open && item.class === "ligand"}
              {#if item.name !== undefined}
                {item.name}
              {:else if item.sdf !== ""}
                SDF file
              {:else}
                {item.smiles}
              {/if}
            {/if}
          </span>
        </div>

        <div class="flex items-center space-x-2">
          <svg
            data-slot="icon"
            fill="none"
            stroke-width="3"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            class="w-4 h-4 text-red-800"
            on:click={(e) => {
              dispatch("removeVal", i);
            }}
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18 18 6M6 6l12 12"
            ></path>
          </svg>

          <svg
            data-accordion-icon
            class="w-3 h-3 shrink-0"
            class:rotate-180={item.open}
            class:-rotate-90={!item.open}
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
              d="M9 5 5 1 1 5"
            />
          </svg>
        </div>
      </button>
    </h2>

    {#if item.open}
      <div
        id={`accordion-collapse-body-${i}`}
        aria-labelledby={`accordion-collapse-heading-${i}`}
      >
        <div
          class="p-5 border border-t-0 border-gray-200 dark:border-gray-700 dark:bg-gray-900"
        >
          {#if ["DNA", "RNA", "protein"].includes(item.class)}
            <textarea
              id="message"
              rows="4"
              class="p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border-1 border-grey-200 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              style="display:block"
              placeholder="MSAVGH..."
              value={item.sequence}
              on:keypress={(e) => {
                if (e.key === "Enter") {
                  if (e.target.value.length != 0) {
                    dispatch("updateVals", {
                      sequence: e.target.value,
                      close: true,
                      index: i,
                    });
                  } else {
                    alert("Sequence is empty");
                  }
                }
              }}
            ></textarea>
            <div class="flex items-center justify-between mt-1">
              <div class="flex items-center space-x-2 text-sm">
                <span>Single sequence</span>

                <label class="relative inline-flex cursor-pointer items-center">
                  <input
                    id="switch"
                    type="checkbox"
                    class="peer sr-only"
                    name={"msa" + i}
                    bind:checked={item.msa}
                  />
                  <label for="switch" class="hidden"></label>
                  <div
                    class="peer h-5 w-9 rounded-full border bg-slate-200 after:absolute after:left-[2px] after:top-0.5 after:h-4 after:w-4 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-slate-800 peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-green-300"
                  ></div>
                </label>
                <span>Use MSA</span>
              </div>
              <div class="text-gray-700">
                Press Enter or <button
                  on:click={() => {
                    if (item.sequence.length != 0) {
                      dispatch("updateVals", {
                        sequence: item.sequence,
                        close: true,
                        index: i,
                      });
                    } else {
                      alert("Sequence is empty");
                    }
                  }}
                  class="hover:bg-gray-100 hover:text-gray-900 underline p-1 rounded"
                  >click to add sequence.</button
                >
              </div>
            </div>
          {:else if item.class === "ligand"}
            <label
              for={"smiles" + i}
              class="block text-sm font-bold mb-1 px-2.5 dark:text-white"
              >SMILES</label
            >
            <textarea
              rows="1"
              class=" p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              style="display:block"
              placeholder="SMILES like CCC ..."
              value={item.smiles}
              name={"smiles" + i}
              on:keypress={(e) => {
                if (e.key === "Enter") {
                  if (e.target.value.length != 0) {
                    dispatch("updateVals", {
                      smiles: e.target.value,
                      close: true,
                      index: i,
                    });
                  } else {
                    alert("Sequence is empty");
                  }
                }
              }}
            ></textarea>
            <div class="text-gray-700 mt-0.5 px-2.5 text-right text-sm">
              Press Enter or <button
                on:click={() => {
                  if (item.smiles != "") {
                    dispatch("updateVals", {
                      smiles: item.smiles,
                      close: true,
                      index: i,
                    });
                  } else {
                    alert("SMILES is empty");
                  }
                }}
                class="hover:bg-gray-100 hover:text-gray-900 underline p-1 rounded"
                >click to add SMILES.</button
              >
            </div>

            <div class="text-center text-gray-400 w-full my-2">- or -</div>

            {#if item.name === "" || item.name == undefined}
              <SearchInput
                database="rcsb-3ligand"
                index={i}
                on:triggerFetch={handleMessage}
              />
            {:else}
              <div class="max-w-lg mx-auto mb-2 my-2">
                <div class="flex">
                  <label
                    for="search-dropdown"
                    class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
                    >Current ligand</label
                  >
                  <button
                    id="dropdown-button"
                    data-dropdown-toggle="dropdown"
                    class="flex-shrink-0 z-10 inline-flex items-center py-2.5 px-4 text-sm font-medium text-center text-gray-900 bg-gray-100 border border-gray-300 rounded-s-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600"
                    type="button"
                    >CCD
                  </button>

                  <div class="relative w-full">
                    <input
                      type="search"
                      id="search-dropdown"
                      class=" p-2.5 w-full h-full z-20 text-sm text-gray-900 bg-gray-50 rounded-e-lg border-s-gray-50 border-s-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-s-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500"
                      style="display:block"
                      value={item.name}
                    />
                    <button
                      on:click={() => {
                        dispatch("updateVals", {
                          name: "",
                          sdf: "",
                          open: true,
                          index: i,
                        });
                      }}
                      class="absolute top-0 end-0 p-2.5 text-sm font-medium h-full text-white bg-red-700 rounded-e-lg border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        class="w-4 h-4"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                        />
                      </svg>

                      <span class="sr-only">Delete</span>
                    </button>
                  </div>
                </div>
              </div>
            {/if}

            <div class="text-center text-gray-400 w-full my-2">- or -</div>
            <label
              for={"sdf" + i}
              class="block text-sm font-bold mb-1 px-2.5 dark:text-white"
              >SDF file</label
            >
            <textarea
              rows="3"
              class="p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              style="display:block"
              placeholder="SDF format 3D molecule ..."
              value={item.sdf}
              name={"sdf" + i}
              on:keypress={(e) => {
                if (e.key === "Enter") {
                  if (e.target.value != "") {
                    dispatch("updateVals", {
                      sdf: e.target.value,
                      close: true,
                      index: i,
                    });
                  } else {
                    alert("SDF is empty");
                  }
                }
              }}
            ></textarea>
            <div class="text-gray-700 mt-0.5 px-2.5 text-right text-sm">
              Press Enter or <button
                on:click={() => {
                  if (item.sdf != "") {
                    dispatch("updateVals", {
                      sdf: item.sdf,
                      close: true,
                      index: i,
                    });
                  } else {
                    alert("SDF file is empty");
                  }
                }}
                class="hover:bg-gray-100 hover:text-gray-900 underline p-1 rounded"
                >click to add SDF file.</button
              >
            </div>

            <div class="text-center text-gray-400 w-full my-2">- or -</div>

            <div class="text-center text-gray-600 font-bold mb-2">
              Metal ion
            </div>

            <div class="flex justify-center space-x-2">
              {#each metals as metal}
                <button
                  class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden rounded-full dark:bg-gray-600"
                  class:bg-blue-200={item.name === metal}
                  class:bg-violet-100={item.name !== metal}
                  on:click={() =>
                    dispatch("updateVals", { name: metal, index: i })}
                >
                  <span class="font-medium text-gray-600 dark:text-gray-300"
                    >{metal}</span
                  >
                </button>
              {/each}
            </div>
          {/if}

          <!-- <div class="text-center text-gray-400 w-full my-2">- or -</div>

          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white hidden"
            for="file_input">Upload file</label
          >
          <input
            class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
            aria-describedby="file_input_help"
            id="file_input"
            type="file"
          />
          <p
            class="mt-1 text-sm text-gray-500 dark:text-gray-300"
            id="file_input_help"
          >
            .fasta files
          </p> -->
        </div>
      </div>
    {/if}
    {#if !item.open}
      {#if ["DNA", "RNA", "protein"].includes(item.class)}
        <div
          id={`accordion-collapse-body-${i}`}
          aria-labelledby={`accordion-collapse-heading-${i}`}
        >
          <div
            class="p-5 border border-t-0 border-gray-200 dark:border-gray-700"
            class:border-b-0={i != vals.length - 1}
          >
            {#if item.sequence !== ""}
              <Sequence seq={item.sequence} />
            {/if}
          </div>
        </div>
      {:else if item.class === "ligand"}
        {#if item.sdf !== ""}
          <div
            class="p-5 border border-t-0 border-gray-200 dark:border-gray-700"
            class:border-b-0={i != vals.length - 1}
          >
            <div class="relative">
              <Molecule
                molvalue={item.sdf}
                showCovMod={showCovModVals[i]}
                on:updateMol={updateMol}
              />
            </div>
          </div>
          <!-- {:else if metals.includes(item.name)}
          {item.name}
        {:else}
          {item.smiles} -->
        {/if}
      {/if}
    {/if}
  {/each}

  <div
    class="p-5 border border-t-0 border-gray-200 dark:border-gray-700 w-full"
  >
    {#if covMods.length > 0}
      <h4 class="text-center font-bold text-xl">Covalent Modification</h4>
      {#each covMods as covMod, i}
        <div class="flex p-10">
          <div class="flex divide-x rounded border p-1 w-full">
            <div class="w-3/5 flex-col px-2">
              <div class="flex justify-center">
                <span class="text-base font-medium text-gray-900">Protein</span>
              </div>
              <div class="grid grid-cols-4 font-bold">
                <span>Chain</span>
                <span>Residue</span>
                <span>Atom</span>
                <span>Chirality</span>
              </div>
              <div class="grid grid-cols-4">
                <select
                  name=""
                  id=""
                  bind:value={covMods[i].protein}
                  on:change={() => dispatch("updateCovMod", covMods)}
                >
                  {#each proteinChains as chain}
                    <option value={chain}>{chain}</option>
                  {/each}
                </select>

                <select
                  name=""
                  id=""
                  bind:value={covMods[i].residue}
                  on:change={() => dispatch("updateCovMod", covMods)}
                >
                  {#each getResidues(covMod) as resi, i}
                    <option value={i + 1}>{i + 1} {resi}</option>
                  {/each}
                </select>

                <select
                  name=""
                  id=""
                  bind:value={covMods[i].atom}
                  on:change={() => dispatch("updateCovMod", covMods)}
                >
                  {#if covMod.residue != ""}
                    {#each getResAtoms(covMod) as atom}}
                      <option value={atom}>{getResname(covMod)}:{atom}</option>
                    {/each}
                  {:else}
                    <option disabled></option>
                  {/if}
                </select>

                <select
                  name=""
                  id=""
                  bind:value={covMods[i].protein_symmetry}
                  on:change={() => dispatch("updateCovMod", covMods)}
                >
                  <option value="">no chirality defined</option>
                  <option value="CW">CW</option>
                  <option value="CCW">CCW</option>
                </select>
              </div>
            </div>

            <div class="w-2/5 px-2">
              <div class="flex-col p-1">
                <div class="flex justify-center">
                  <span
                    class="w-full whitespace-nowrap text-center text-base font-medium text-gray-900"
                    >Small molecule</span
                  >
                </div>
                <div class="grid grid-cols-3 font-bold">
                  <span>Chain</span>
                  <span title="click on atom in structure">Atom index </span>

                  <span>Chirality</span>
                </div>
                <div class="grid grid-cols-3">
                  <select
                    name=""
                    id=""
                    title="click on atom in structure"
                    bind:value={covMods[i].ligand}
                    on:change={() => dispatch("updateCovMod", covMods)}
                  >
                    {#each ligandChains as chain}
                      <option value={chain} selected={chain === covMod.ligand}
                        >{chain}</option
                      >
                    {/each}
                  </select>
                  <div>
                    {#if covMod.attachmentIndex}
                      <p class="font-mono">index {covMod.attachmentIndex}</p>
                    {:else}
                      <p class="font-mono">click on atom</p>
                    {/if}
                  </div>

                  <select
                    name=""
                    id=""
                    bind:value={covMods[i].ligand_symmetry}
                    on:change={() => dispatch("updateCovMod", covMods)}
                  >
                    <option value="">no chirality defined</option>
                    <option value="CW">CW</option>
                    <option value="CCW">CCW</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center p-2">
            <svg
              data-slot="icon"
              fill="none"
              stroke-width="2"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
              class="w-8 h-8 text-red-800 cursor-pointer"
              on:click={(e) => {
                dispatch("removeCovMod", i);
              }}
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18 18 6M6 6l12 12"
              ></path>
            </svg>
          </div>
        </div>
      {/each}
    {/if}
  </div>
  <!-- 
  <h2 id="accordion-collapse-heading-2">
    <button
      type="button"
      class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-b-0 border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
      data-accordion-target="#accordion-collapse-body-2"
      aria-expanded="false"
      aria-controls="accordion-collapse-body-2"
    >
      <div>
        <span
          class="inline-flex items-center justify-center p-1 px-2 text-xs font-semibold text-blue-800 bg-blue-200 rounded-full"
        >
          A
        </span>
        <span>NA sequence</span>
      </div>
      <svg
        data-accordion-icon
        class="w-3 h-3 -rotate-90 shrink-0"
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
          d="M9 5 5 1 1 5"
        />
      </svg>
    </button>
    <div class="px-2">
      <Sequence />
    </div>
  </h2>

  <div
    id="accordion-collapse-body-2"
    class="hidden"
    aria-labelledby="accordion-collapse-heading-2"
  >
    <div
      class="p-5 border border-b-0 border-gray-200 dark:border-gray-700"
    ></div>
  </div>
  <h2 id="accordion-collapse-heading-3">
    <button
      type="button"
      class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
      data-accordion-target="#accordion-collapse-body-3"
      aria-expanded="false"
      aria-controls="accordion-collapse-body-3"
    >
      <div>
        <span
          class="inline-flex items-center justify-center p-1 px-2 text-xs font-semibold text-blue-800 bg-orange-200 rounded-full"
        >
          C
        </span>
        <span>Small molecule</span>
      </div>
      <svg
        data-accordion-icon
        class="w-3 h-3 rotate-180 shrink-0"
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
          d="M9 5 5 1 1 5"
        />
      </svg>
    </button>
  </h2>
  <div
    id="accordion-collapse-body-3"
    aria-labelledby="accordion-collapse-heading-3"
  >
    <div class="p-5 border border-t-0 border-gray-200 dark:border-gray-700">
      <label
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        for="file_input">Upload file</label
      >
      <input
        class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
        aria-describedby="file_input_help"
        id="file_input"
        type="file"
      />
      <p
        class="mt-1 text-sm text-gray-500 dark:text-gray-300"
        id="file_input_help"
      >
        SVG, PNG, JPG or GIF (MAX. 800x400px).
      </p>
      <div class="text-center text-gray-400 w-full my-2">- or -</div>

      <textarea
        id="message"
        rows="4"
        class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="SMILES like CCC ..."
      ></textarea>

      <div class="text-center text-gray-400 w-full my-2">- or -</div>

      <SearchInput database="rcsb-3ligand" />

      <div class="text-center text-gray-400 w-full my-2">- or -</div>

      <div class="text-center text-gray-600 font-bold mb-2">Metal ion</div>
      <div class="flex justify-center space-x-2">
        <div
          class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-violet-100 rounded-full dark:bg-gray-600"
        >
          <span class="font-medium text-gray-600 dark:text-gray-300">ZN</span>
        </div>

        <div
          class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-green-100 rounded-full dark:bg-gray-600"
        >
          <span class="font-medium text-gray-600 dark:text-gray-300">MG</span>
        </div>

        <div
          class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-green-100 rounded-full dark:bg-gray-600"
        >
          <span class="font-medium text-gray-600 dark:text-gray-300">CA</span>
        </div>

        <div
          class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-violet-100 rounded-full dark:bg-gray-600"
        >
          <span class="font-medium text-gray-600 dark:text-gray-300">FE</span>
        </div>

        <div
          class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-yellow-100 rounded-full dark:bg-gray-600"
        >
          <span class="font-medium text-gray-600 dark:text-gray-300">NA</span>
        </div>
      </div>
    </div>
  </div> 

   -->
</div>
