--[[
dobozok.lua -- egységes, arculatos kiemelődobozok minden kimeneti formátumra
(a PE nyílt tankönyvsorozat közös szűrője).

Markdownban:
  ::: {.eset eset="A" title="ReaktorVéd: mi a csúcsesemény?"}
  szöveg ...
  :::

Típusok: cel, fogalom, eset, pelda, kitekintes, hiba, onell, projekt, prompt,
         osszefoglalo, forras, labor, baleset.
Az önellenőrző dobozban egy {.megoldas} blokk HTML-ben lenyitható, PDF-ben
kisebb betűvel, a kérdések után jelenik meg.
]]

local alapcim = {
  cel = "Tanulási eredmények",
  fogalom = "Fogalom",
  eset = "Futó eset",
  pelda = "Kidolgozott példa",
  kitekintes = "Kitekintés",
  hiba = "Gyakori buktató",
  onell = "Önellenőrzés",
  projekt = "Projektlépés",
  prompt = "Mintaprompt",
  osszefoglalo = "Összefoglalás",
  forras = "Továbbolvasás",
  labor = "Gyakorlat",
  baleset = "Esettanulmány egy balesetből",
}

local sorrend = { "cel", "fogalom", "eset", "pelda", "kitekintes", "hiba", "onell",
  "projekt", "prompt", "osszefoglalo", "forras", "labor", "baleset" }

local function latex_escape(s)
  s = s:gsub("\\", "\\textbackslash{}")
  s = s:gsub("([%%#&_%$])", "\\%1")
  s = s:gsub("~", "\\textasciitilde{}")
  return s
end

local function html_escape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

local function is_latex() return quarto.doc.is_format("latex") end
local function is_html() return quarto.doc.is_format("html") end

local function megoldas(el)
  if is_latex() then
    local b = { pandoc.RawBlock("latex", "\\begin{pemegoldas}") }
    for _, x in ipairs(el.content) do table.insert(b, x) end
    table.insert(b, pandoc.RawBlock("latex", "\\end{pemegoldas}"))
    return b
  elseif is_html() then
    local b = { pandoc.RawBlock("html", '<details class="megoldas"><summary>Megoldás</summary>') }
    for _, x in ipairs(el.content) do table.insert(b, x) end
    table.insert(b, pandoc.RawBlock("html", "</details>"))
    return b
  else
    local b = { pandoc.Para({ pandoc.Strong({ pandoc.Str("Megoldás") }) }) }
    for _, x in ipairs(el.content) do table.insert(b, x) end
    return { pandoc.Div(b, pandoc.Attr("", { "megoldas" })) }
  end
end

local function belso(el)
  return pandoc.walk_block(el, { Div = function(d)
    if d.classes:includes("megoldas") then return megoldas(d) end
  end })
end

function Div(el)
  if el.classes:includes("megoldas") then
    return megoldas(el)
  end
  for _, tipus in ipairs(sorrend) do
    if el.classes:includes(tipus) then
      local cim = alapcim[tipus]
      local title = el.attributes["title"] or cim
      local eset = el.attributes["eset"]
      local kulcs = tipus
      if tipus == "eset" and eset then
        kulcs = "eset" .. eset
        if not el.attributes["title"] then title = "Futó eset " .. eset end
      end
      el = belso(el)
      local tartalom = el.content
      if is_latex() then
        -- dobozon belül nem lehet úszó objektum: az ábrák helyben ([H]) jelennek meg
        tartalom = pandoc.Blocks(tartalom):walk({
          Figure = function(f) f.attributes["fig-pos"] = "H"; return f end,
          Image = function(i) i.attributes["fig-pos"] = "H"; return i end })
        local b = { pandoc.RawBlock("latex",
          "\\begin{pedoboz}{" .. kulcs .. "}{" .. latex_escape(title) .. "}\\pefigurahelyben") }
        for _, x in ipairs(tartalom) do table.insert(b, x) end
        table.insert(b, pandoc.RawBlock("latex", "\\end{pedoboz}"))
        return b
      elseif is_html() then
        local b = { pandoc.RawBlock("html",
          '<div class="doboz doboz-' .. kulcs .. '"><div class="doboz-cim">' ..
          html_escape(title) .. '</div><div class="doboz-tartalom">') }
        for _, x in ipairs(tartalom) do table.insert(b, x) end
        table.insert(b, pandoc.RawBlock("html", "</div></div>"))
        return b
      else
        local b = { pandoc.Para({ pandoc.Strong({ pandoc.Str(title) }) }) }
        for _, x in ipairs(tartalom) do table.insert(b, x) end
        return { pandoc.Div(b, pandoc.Attr("", { "doboz", "doboz-" .. kulcs })) }
      end
    end
  end
end
