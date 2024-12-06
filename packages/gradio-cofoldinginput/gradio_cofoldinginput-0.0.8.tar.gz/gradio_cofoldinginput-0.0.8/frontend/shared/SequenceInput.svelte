<svelte:options accessors={true} />

<script>
  import { tick } from "svelte";

  import Btn from "./Button.svelte";
  import SearchInput from "./SearchInput.svelte";

  import Accordion from "./Accordion.svelte";
  import { createEventDispatcher, onMount, afterUpdate } from "svelte";

  // import "../style.css";

  export let value = { chains: [], covMods: [] };

  const dispatch = createEventDispatcher();

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

  async function getSDF(id) {
    let sdf = await fetch(
      `https://files.rcsb.org/ligands/download/${id}_ideal.sdf`
    )
      .then((response) => {
        if (!response.ok) {
          // Check if the status code is 200
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .catch((error) => {
        alert("Error fetching sdf file");
      });
    // console.log(sdf);
    return sdf;
  }

  function nextChainTemp(currentChain) {
    if (currentChain == "") {
      return "A";
    }
    let nextChain = "";
    if (currentChain == "Z") {
      nextChain = "AA";
    } else if (currentChain.length > 1 && currentChain.slice(-1) === "Z") {
      nextChain = String.fromCharCode(currentChain.charCodeAt(0) + 1) + "A";
    } else {
      nextChain =
        currentChain.slice(0, -1) +
        String.fromCharCode(currentChain.slice(-1).charCodeAt(0) + 1);
    }
    return nextChain;
  }
  async function handleMessage(event) {
    let pdbId = event.detail.text;
    //convert to lowercase
    pdbId = pdbId.toLowerCase();
    let bioAssemblyInfo = await importBioAssembly(pdbId);
    // console.log(bioAssemblyInfo);
    // convert assembly info to vals
    let tempVals = [];
    let nextChain = "";

    let promise = await Promise.all(
      bioAssemblyInfo.map(async (entity) => {
        if (["DNA", "RNA", "protein"].includes(entity.class)) {
          for (let i = 0; i < entity.count; i++) {
            nextChain = nextChainTemp(nextChain);
            tempVals.push({
              class: entity.class,
              name: "",
              smiles: "",
              sdf: "",
              sequence: entity.entityInfo,
              open: false,
              chain: nextChain,
            });
            await tick();
          }
        } else if (entity.class === "ligand") {
          let name = "";
          let sdf = "";
          if (metals.includes(entity.entityInfo)) {
            name = entity.entityInfo;
          } else {
            sdf = await getSDF(entity.entityInfo);
          }
          for (let i = 0; i < entity.count; i++) {
            nextChain = nextChainTemp(nextChain);
            tempVals.push({
              class: entity.class,
              name: name,
              smiles: "",
              sdf: sdf,
              sequence: "",
              open: false,
              chain: nextChain,
            });
          }
          await tick();
        }
      })
    );
    vals = tempVals;
    dispatch("updateVals", vals);
  }

  let vals = [];
  let covMods = [];

  function update(event) {
    // console.log(vals[event.detail.index]);
    if (event.detail.sequence !== undefined) {
      vals[event.detail.index].sequence = event.detail.sequence;
    }
    if (event.detail.name !== undefined) {
      vals[event.detail.index].name = event.detail.name;
    } else {
      vals[event.detail.index].name = "";
    }
    if (event.detail.smiles !== undefined) {
      vals[event.detail.index].smiles = event.detail.smiles;
    } else {
      vals[event.detail.index].smiles = "";
    }
    if (event.detail.sdf !== undefined) {
      vals[event.detail.index].sdf = event.detail.sdf;
    } else {
      vals[event.detail.index].sdf = "";
    }
    if (event.detail.close == true) {
      vals[event.detail.index].open = false;
    } else {
      vals[event.detail.index].open = true;
    }

    dispatch("updateVals", vals);
  }

  function getNextChainLetter() {
    let highestChainLetter = "A";
    for (let val of vals) {
      if (val.chain > highestChainLetter) {
        highestChainLetter = val.chain;
      }
    }

    // Increment the highest chain letter to get the next chain letter
    let nextChainLetter = "";
    if (highestChainLetter < "Z") {
      nextChainLetter = String.fromCharCode(
        highestChainLetter.charCodeAt(0) + 1
      );
    } else {
      let lastChar = highestChainLetter.slice(-1);
      if (lastChar < "Z") {
        nextChainLetter =
          highestChainLetter.slice(0, -1) +
          String.fromCharCode(lastChar.charCodeAt(0) + 1);
      } else {
        nextChainLetter = highestChainLetter + "A";
      }
    }

    return nextChainLetter;
  }

  function insertChain(event) {
    // what chain to add next
    let nextChainLetter = getNextChainLetter();
    vals.push({
      class: event.detail.type,
      name: "",
      smiles: "",
      sdf: "",
      sequence: "",
      open: true,
      chain: nextChainLetter,
      msa: true,
    });
    vals = vals;
    // console.log(vals);
  }

  function remove(event) {
    vals.splice(event.detail, 1);
    vals = vals;
    dispatch("updateVals", vals);
  }

  async function fetchMolecules(pdbId) {
    const url = `https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/${pdbId}`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(
          `Error fetching molecules for PDB ID ${pdbId}: ${response.statusText}`
        );
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching molecules:", error);
    }
  }

  async function fetchXmlText(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error fetching XML: ${response.statusText}`);
      }
      const textData = await response.text();
      return textData;
    } catch (error) {
      console.error("Error fetching XML:", error);
    }
  }

  // Function to parse a single assembly element
  function parseAssembly(assemblyElement) {
    const assembly = {
      id: assemblyElement.getAttribute("id"),
      composition: assemblyElement.getAttribute("composition"),
      molecularWeight: assemblyElement.getAttribute("molecular_weight"),
      name: assemblyElement.getAttribute("name"),
    };
    const entities = [];
    assemblyElement.querySelectorAll("entity").forEach((entityElement) => {
      entities.push({
        chainIds: entityElement.getAttribute("chain_ids"),
        class: entityElement.getAttribute("class"),
        count: entityElement.getAttribute("count"),
        entityId: Number(entityElement.getAttribute("entity_id")), // Added entityId
      });
    });
    assembly.entities = entities;
    return assembly;
  }

  function extractEntityInfo(entity, moleculeData) {
    if (
      entity.class === "DNA" ||
      entity.class === "RNA" ||
      entity.class === "protein"
    ) {
      // find the entry in moleculedata that matches the entity ID
      const matchingEntity = moleculeData.find(
        (molecule) => molecule.entity_id === entity["entityId"]
      );
      if (matchingEntity) {
        return matchingEntity.sequence;
      }
    } else {
      const matchingEntity = moleculeData.find(
        (molecule) => molecule.entity_id === entity["entityId"]
      );
      if (matchingEntity) {
        // return the sequence of the matching entity
        return matchingEntity.chem_comp_ids[0];
      }
    }
  }

  function importBioAssembly(pdbId) {
    const moleculeData = fetchMolecules(pdbId)
      .then((data) => {
        return data;
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    // Example usage
    const xmlUrl = `https://www.ebi.ac.uk/pdbe/static/entry/${pdbId}-assembly.xml`;
    const assemblies = fetchXmlText(xmlUrl).then((data) => {
      // Parse the entire assembly list
      const assemblyList = [];
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, "text/xml");
      const assemblyElements = doc.querySelectorAll("assembly");
      assemblyElements.forEach((assemblyElement) => {
        assemblyList.push(parseAssembly(assemblyElement));
      });

      return assemblyList;
    });

    // wait for both fetches to complete
    let result = Promise.all([moleculeData, assemblies]).then(
      ([moleculeData, assemblies]) => {
        let bioAssemblyInfo = [];

        let assembly = assemblies[0];
        assembly.entities.forEach((entity) => {
          const entityInfo = extractEntityInfo(entity, moleculeData[pdbId]);
          bioAssemblyInfo.push({
            class: entity.class,
            entityInfo: entityInfo,
            count: entity.count,
          });
        });

        return bioAssemblyInfo;
      }
    );
    return result;
  }
  let display = false;

  function addCovMod(event) {
    let firstProteinChain = vals.find((val) => val.class === "protein").chain;

    if (firstProteinChain === undefined) {
      alert("Please add a protein chain first");
      return;
    }
    let firstLigandChain = vals.find((val) => val.class === "ligand").chain;

    if (firstLigandChain === undefined) {
      alert("Please add a ligand chain first");
      return;
    }
    let covMod = {
      protein: firstProteinChain,
      residue: "1",
      atom: "N",
      protein_symmetry: "CW",
      ligand: firstLigandChain,
      attachmentIndex: 1,
      deleteIndexes: [],
      ligand_symmetry: "CW",
    };
    covMods.push(covMod);
    covMods = covMods;
    vals = vals;
    dispatch("updateCovMod", covMods);
  }

  function removeCovMod(event) {
    covMods.splice(event.detail, 1);
    covMods = covMods;
  }
  function syncCovMod(event) {
    covMods = event.detail;
    dispatch("updateCovMod", covMods);
  }

  onMount(async () => {
    vals = value["chains"];
    covMods = value["covMods"];
    // vals = value["chains"];
  });

  // for each change of value, update vals and covMods
  let old_value = value;
  $: if (JSON.stringify(old_value) !== JSON.stringify(value)) {
    vals = value["chains"];
    covMods = value["covMods"];
    old_value = value;
  }
</script>

{#if vals != undefined}
  {#if vals.length > 0}
    <Accordion
      {vals}
      {covMods}
      on:updateVals={update}
      on:removeVal={remove}
      on:removeCovMod={removeCovMod}
      on:updateCovMod={syncCovMod}
    />
  {:else}
    <div class="my-8 text-center text-gray-600">Empty input</div>

    <div class="text-center text-gray-400">
      You can import a protein from the PDB
    </div>
    <SearchInput database="rcsb-bioass" on:triggerFetch={handleMessage} />

    <div class="text-center text-gray-400 w-full my-2">
      - or create the input from scratch -
    </div>
  {/if}
{/if}
<Btn
  {vals}
  on:addNewChain={insertChain}
  on:addCovalentModification={addCovMod}
/>
