<template>
  <section style="overflow: visible !important; position: relative !important; z-index: 1000 !important;">
  <link rel="stylesheet"
    type="text/css"
    href="https://fonts.googleapis.com/icon?family=Material+Icons"
  />

  <link
    v-for="link in args.links"
    rel="stylesheet"
    type="text/css"
    :href="link"
  />

  <component v-if="css" :is="'style'">
      {{ css }}
  </component>

  <nav
      class="navbar"
      :class="{ 'has-active-dropdown': hasActiveDropdown }"
      :style="parseStyles(styles['nav'])">
    <div
      class="navbar-left navbar-group"
      :style="parseStyles(styles['div'])">
      <ul :style="parseStyles(styles['ul'])"
	class="navbar-list">
        <li
          v-if="args.base64_svg"
          :style="parseStyles(styles['li'])"
	  class="navbar-item"
        >
          <a
            v-if="args.logo_page"
            href="#"
	    class="navbar-anchor"
            :style="parseStyles(styles['a'])"
            @click="onClicked(args.logo_page)"
          >
            <img
              :src="`data:image/svg+xml; base64, ${args.base64_svg}`"
              :style="parseStyles(styles['img'])"
            />
          </a>
          <a
            v-else-if="args.logo_page === null"
	    class="navbar-anchor"
            :style="parseStyles(styles['a'])"
          >
            <img
	      class="navbar-logo"
              :src="`data:image/svg+xml; base64, ${args.base64_svg}`"
              :style="parseStyles(styles['img'])"
            />
          </a>
        </li>

        <!-- Show submenu items when hovering over a parent, otherwise show main items -->
        <template v-if="!hasActiveDropdown">
          <!-- Normal main menu items -->
          <li
            v-for="page in args.left"
            class="navbar-item"
            :class="{ 'has-submenu': page.submenu && page.submenu.length > 0 }"
            :key="page.title"
            :style="parseStyles(styles['li'])"
            @mouseenter="handleMenuHover(page)"
            @mouseleave="hideDropdown(page)"
          >
            <a
              :href="page.url[0]"
              :target="page.url[1]"
              :style="parseStyles(styles['a'])"
              class="navbar-anchor"
              @click="onClicked(page)"
            >
              <span
                :data-text="page.title"
                :class="[{active: page.key === activePage}, hoverColor, hoverBgColor]"
                :style="parseStyles(styles['span']) + parseStyles(styles['active'], page.key === activePage)"
                class="navbar-span"
                style="display: inline-block;"
              >
                <div
                  v-if="page.icon"
                  class="material-icons navbar-icon"
                  style="display: inline; vertical-align: middle"
                >
                  {{ page.icon }}
                </div>
                <div class="navbar-text" style="display: inline; vertical-align: middle; margin-left: 0.35em">
                  {{ page.title }}
                  <span v-if="page.submenu && page.submenu.length > 0" class="submenu-arrow">▼</span>
                </div>
              </span>
            </a>
          </li>
        </template>

        <template v-else>
          <!-- Show submenu items when hovering -->
          <li
            v-for="(page, pageIndex) in args.left"
            :key="`hover-${page.title}`"
            class="navbar-item submenu-container"
            :style="parseStyles(styles['li'])"
            @mouseenter="handleMenuHover(page)"
            @mouseleave="hideDropdown(page)"
          >
            <template v-if="dropdownVisible[page.key] && page.submenu">
              <!-- Show submenu items for the hovered parent -->
              <a
                v-for="subItem in page.submenu"
                :key="subItem.key"
                :href="subItem.url[0]"
                :target="subItem.url[1]"
                :style="parseStyles(styles['a'])"
                class="navbar-anchor submenu-item"
                @click="onClicked(subItem)"
              >
                <span
                  :class="[{active: subItem.key === activePage}, hoverColor, hoverBgColor]"
                  :style="parseStyles(styles['span'])"
                  class="navbar-span"
                  style="display: inline-block; margin: 0 0.25rem;"
                >
                  <div
                    v-if="subItem.icon"
                    class="material-icons navbar-icon"
                    style="display: inline; vertical-align: middle; font-size: 0.9rem;"
                  >
                    {{ subItem.icon }}
                  </div>
                  <div class="navbar-text" style="display: inline; vertical-align: middle; margin-left: 0.25em; font-size: 0.9rem;">
                    {{ subItem.title }}
                  </div>
                </span>
              </a>
            </template>
            <template v-else-if="!hasActiveDropdown">
              <!-- Show normal menu item -->
              <a
                :href="page.url[0]"
                :target="page.url[1]"
                :style="parseStyles(styles['a'])"
                class="navbar-anchor"
                @click="onClicked(page)"
              >
                <span
                  :data-text="page.title"
                  :class="[{active: page.key === activePage}, hoverColor, hoverBgColor]"
                  :style="parseStyles(styles['span']) + parseStyles(styles['active'], page.key === activePage)"
                  class="navbar-span"
                  style="display: inline-block;"
                >
                  <div
                    v-if="page.icon"
                    class="material-icons navbar-icon"
                    style="display: inline; vertical-align: middle"
                  >
                    {{ page.icon }}
                  </div>
                  <div class="navbar-text" style="display: inline; vertical-align: middle; margin-left: 0.35em">
                    {{ page.title }}
                    <span v-if="page.submenu && page.submenu.length > 0" class="submenu-arrow">▼</span>
                  </div>
                </span>
              </a>
            </template>
          </li>
        </template>
      </ul>
    </div>
    <div
      v-if="args.right.length"
      class="navbar-right navbar-group"
      :style="parseStyles(styles['div'])">
      <ul :style="parseStyles(styles['ul'])"
	class="navbar-list">
        <template v-for="page in args.right" :key="page.title">
          <li
            v-if="hasActiveDropdown && dropdownVisible[page.key] && page.submenu && page.submenu.length > 0"
            v-for="subItem in page.submenu"
            :key="subItem.key"
            class="navbar-item submenu-item"
            :style="parseStyles(styles['li'])"
          >
            <a
              :href="subItem.url[0]"
              :target="subItem.url[1]"
              :style="parseStyles(styles['a'])"
              class="navbar-anchor"
              @click="onClicked(subItem)"
            >
              <span
                :class="[{active: subItem.key === activePage}, hoverColor, hoverBgColor]"
                :style="parseStyles(styles['span'])"
                class="navbar-span"
                style="display: inline-block; margin: 0 0.25rem;"
              >
                <div
                  v-if="subItem.icon"
                  class="material-icons navbar-icon"
                  style="display: inline; vertical-align: middle; font-size: 0.9rem;"
                >
                  {{ subItem.icon }}
                </div>
                <div class="navbar-text" style="display: inline; vertical-align: middle; margin-left: 0.25em; font-size: 0.9rem;">
                  {{ subItem.title }}
                </div>
              </span>
            </a>
          </li>
          <li
            v-else-if="!hasActiveDropdown"
            class="navbar-item"
            :class="{ 'has-submenu': page.submenu && page.submenu.length > 0 }"
            :style="parseStyles(styles['li'])"
            @mouseenter="handleMenuHover(page)"
            @mouseleave="hideDropdown(page)"
          >
            <a
              :href="page.url[0]"
              :target="page.url[1]"
              :style="parseStyles(styles['a'])"
              class="navbar-anchor"
              @click="onClicked(page)"
            >
              <span
                :data-text="page.title"
                :class="[{active: page.key === activePage}, hoverColor, hoverBgColor]"
                :style="parseStyles(styles['span']) + parseStyles(styles['active'], page.key === activePage)"
                class="navbar-span"
                style="display: inline-block;"
              >
                <div
                  v-if="page.icon"
                  class="material-icons navbar-icon"
                  style="display: inline; vertical-align: middle"
                >
                  {{ page.icon }}
                </div>
                <div class="navbar-text" style="display: inline; vertical-align: middle; margin-left: 0.35em">
                  {{ page.title }}
                  <span v-if="page.submenu && page.submenu.length > 0" class="submenu-arrow">▼</span>
                </div>
              </span>
            </a>
          </li>
        </template>
      </ul>
    </div>
  </nav>
  </section>
</template>

<script setup>
import { ref, computed, watch, reactive } from "vue"
import { Streamlit } from "streamlit-component-lib"
import { useStreamlit } from "./streamlit"

// Arguments that are passed to the plugin in Python are accessible in props
// "args".
const props = defineProps(["args"])
// Fetch changes to the default page, made by a callback function.
const selected = computed(() => props.args.default[0])
const activePage = ref(props.args.default[0])
const dropdownVisible = reactive({})

// Check if any dropdown is currently visible
const hasActiveDropdown = computed(() => {
  return Object.values(dropdownVisible).some(visible => visible)
})

// Initialize dropdown visibility for all pages with submenus
const initializeDropdowns = () => {
  const allPages = [...props.args.left, ...props.args.right];
  allPages.forEach(page => {
    if (page.submenu && page.submenu.length > 0) {
      dropdownVisible[page.key] = false;
    }
  });
}

initializeDropdowns();

// Debug logs removed for cleaner console

useStreamlit()  // Lifecycle hooks for automatic Streamlit resize.

watch(selected, () => {
    // Executed when `selected` changes.
    activePage.value = selected.value
    console.log("active page", activePage)
  }
)

let hoverTimeout = null;

const clearAllDropdowns = () => {
  // Clear all active dropdowns
  for (const key in dropdownVisible) {
    dropdownVisible[key] = false;
  }
}

const showDropdown = (page) => {
  // Clear any pending hide timeout
  if (hoverTimeout) {
    clearTimeout(hoverTimeout);
    hoverTimeout = null;
  }

  // First clear all other dropdowns
  clearAllDropdowns();

  // Then show the current one if it has a submenu
  if (page.submenu && page.submenu.length > 0) {
    dropdownVisible[page.key] = true;
  }
}

const hideDropdown = (page) => {
  // Add a small delay to prevent flickering when moving between elements
  hoverTimeout = setTimeout(() => {
    if (page.submenu && page.submenu.length > 0) {
      dropdownVisible[page.key] = false;
    }
    hoverTimeout = null;
  }, 100);
}

const handleMenuHover = (page) => {
  // This function is called for ALL menu items (with or without submenus)
  // Clear any pending hide timeout
  if (hoverTimeout) {
    clearTimeout(hoverTimeout);
    hoverTimeout = null;
  }

  // Clear all dropdowns first
  clearAllDropdowns();

  // Then show dropdown only if this item has a submenu
  if (page.submenu && page.submenu.length > 0) {
    dropdownVisible[page.key] = true;
  }
}

const onClicked = (page) => {
  /* remove the object proxy, so we can return it via streamlit */
  const p = JSON.parse(JSON.stringify(page));
  if (p === props.args.logo_page) {
    activePage.value = p;
    const time = props.args.allow_reselect ? Date.now() : null;
    Streamlit.setComponentValue([p, time]);
  } else if (p.url[0] === "#") {
    activePage.value = p.key;
    const time = props.args.allow_reselect ? Date.now() : null;
    Streamlit.setComponentValue([p.key, time]);
  }
}


const styles = ref(props.args.styles || {})
const css = ref(props.args.css)

const parseStyles = (dictionary, condition) => {
  if (typeof condition === "undefined") {
    condition = true
  }
  if (!condition) {
    return ""
  }
  let styleString = ""
  for (const key in dictionary) {
    styleString += `${key}:${dictionary[key]};`
  }
  return styleString
}

let color = ""
let bgColor = ""
if ("hover" in styles.value) {
  const stylesHover = styles.value["hover"]
  if ("color" in stylesHover) {
    color = stylesHover["color"]
  }
  if ("background-color" in stylesHover) {
    bgColor = stylesHover["background-color"]
  }
}
let hoverColor = ""
if (!(color === "")) {
  hoverColor = ref("hover-color")
}
let hoverBgColor = ""
if (!(bgColor === "")) {
  hoverBgColor = ref("hover-bg-color")
}
</script>

<style scoped>
@layer default {
div.navbar-right > ul {
  justify-content: right;
}

/* HTML tags */
* {
  margin: 0;
  padding: 0;
}
nav {
  align-items: center;  /* Back to center alignment */
  background-color: var(--secondary-background-color);
  display: flex;
  font-family: var(--font);
  height: 2.875rem;  /* Back to normal height */
  justify-content: center;
  padding-left: 2rem;
  padding-right: 2rem;
  position: relative;
  overflow: visible !important;
}

div.navbar-left, div.navbar-right {
  max-width: 43.75rem;
  width: 100%;
}
ul {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
li {
  align-items: center;
  display: flex;
  list-style: none;
  position: relative;
}
a {
  text-decoration: none;
}
img {
  display: flex;
  height: 1.875rem;
}

span.navbar-span {
  color: var(--text-color);
}

div.navbar-text {
  display: block;
  text-align: center;
}

/* Special class that acts as an :active pseudo-class for <span> */
.active {
  color: var(--text-color);
  -webkit-text-stroke-width: 0.5px;
}

/* Both classes with :hover direct the style to <span> */
.hover-color:hover {
  color: v-bind(color) !important;
}
.hover-bg-color:hover {
  background-color: v-bind(bgColor) !important;
}

/* Submenu styling */
.submenu-arrow {
  font-size: 0.6em;
  margin-left: 0.5em;
  transition: transform 0.2s ease-in-out;
}

.has-submenu:hover .submenu-arrow {
  transform: rotate(180deg);
}

.submenu-container {
  display: flex;
  align-items: center;
}

.submenu-item {
  margin: 0 0.1rem;
}
}
</style>
