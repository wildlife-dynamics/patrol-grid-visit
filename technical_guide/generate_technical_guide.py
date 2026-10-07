"""
Generate the Patrol Grid Visit Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: patrol_grid_visit_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "patrol_grid_visit_technical_guide.pdf"

# ── Colour palette ────────────────────────────────────────────────────────────
GREEN_DARK   = colors.HexColor("#115631")
GREEN_MID    = colors.HexColor("#2d6a4f")
GREEN_LIGHT  = colors.HexColor("#d8f3dc")
AMBER        = colors.HexColor("#e7a553")
SLATE        = colors.HexColor("#3d3d3d")
LIGHT_GREY   = colors.HexColor("#f5f5f5")
MID_GREY     = colors.HexColor("#cccccc")
WHITE        = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE     = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                   spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE  = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                   spaceAfter=4,  alignment=TA_CENTER)
META      = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                   alignment=TA_CENTER, spaceAfter=2)

H1        = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                   spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold",
                   borderPad=0)
H2        = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                   spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3        = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                   spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")

BODY      = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                   spaceAfter=6, alignment=TA_JUSTIFY)
BULLET    = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                   spaceAfter=3, leftIndent=14, firstLineIndent=-10,
                   bulletIndent=4)
CODE      = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                   backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                   spaceAfter=4, leftIndent=10, rightIndent=10,
                   borderPad=3)
NOTE      = _style("Note", fontSize=8.5, leading=13, textColor=colors.HexColor("#555555"),
                   backColor=colors.HexColor("#fff8e1"), leftIndent=10,
                   rightIndent=10, spaceAfter=6, borderPad=4)
CELL      = _style("Cell", fontSize=8.5, leading=11, textColor=SLATE)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):
    return Paragraph(text, style)

def h1(text): return Paragraph(text, H1)
def h2(text): return Paragraph(text, H2)
def h3(text): return Paragraph(text, H3)
def sp(n=6):  return Spacer(1, n)
def bullet(text): return Paragraph(f"• {text}", BULLET)
def note(text):   return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code(text):   return Paragraph(text, CODE)

def table(data, col_widths, header_row=True):
    # Wrap body cells in Paragraphs so long text flows within the column width.
    rows = [data[0]] + [[Paragraph(str(c), CELL) for c in row] for row in data[1:]]
    t = Table(rows, colWidths=col_widths, repeatRows=1 if header_row else 0)
    style = [
        ("BACKGROUND",  (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",   (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",        (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0, 0), (-1, -1), 6),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0,0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Footer bar
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "Patrol Grid Visit — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    # Top accent line
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="Patrol Grid Visit — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover / Title ─────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Patrol Grid Visit", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Patrol Coverage Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Guide version 1.1  ·  Workflow version 1.0.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        p("Author: Tevin Temu, Wildlife Dynamics", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"),
        hr(),
        p(
            "The <b>Patrol Grid Visit</b> workflow measures how often each part of a "
            "landscape is visited by ranger patrols. It pulls the GPS tracks of completed "
            "patrols from <b>EarthRanger</b>, cleans them into trajectory segments, lays a "
            "regular square grid over the patrolled area, and counts the number of "
            "<b>distinct patrols</b> that passed through each grid cell. The result is a "
            "colour-classified coverage map, delivered as an interactive HTML map and a "
            "single-widget dashboard."
        ),
        p(
            "The workflow is implemented as an <b>Ecoscope Workflow</b> (YAML spec) and "
            "executes within the <code>ecoscope-platform</code> task/compiler runtime. Each "
            "task in the spec is a composable, versioned function; tasks are chained via data "
            "references (<code>${{ workflow.&lt;id&gt;.return }}</code>) and the engine "
            "resolves execution order automatically."
        ),
        h3("Workflow details"),
        table(
            [
                ["Field", "Value"],
                ["Name", "Patrol Grid Visit"],
                ["Workflow version", "1.0.0"],
                ["Author", "Tevin Temu (Wildlife Dynamics) — tevin@wildlifedynamics.com"],
                ["Data source", "EarthRanger (completed patrols)"],
                ["Repository", "github.com/wildlife-dynamics/patrol-grid-visit"],
                ["License", "BSD 3-Clause"],
            ],
            [4*cm, 12.5*cm],
        ),
        sp(4),
        note(
            "The map shows <i>how many different patrols</i> entered each cell, not how many "
            "GPS fixes fall inside it. A single long patrol that loops through a cell "
            "several times still counts once for that cell."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All patrol data is sourced from an <b>EarthRanger</b> instance "
            "(<code>set_er_connection</code> task). The user selects a pre-configured "
            "EarthRanger data source; the resulting client is passed to "
            "<code>get_patrol_observations</code>. Authentication is handled by the "
            "Ecoscope EarthRanger client; no credentials are stored in the spec."
        ),

        sp(4), h2("2.2 Patrol Selection"),
        p(
            "<code>get_patrol_observations</code> fetches the track points recorded during "
            "patrols in the analysis time range. Only the <b>Patrol Types</b> field is "
            "exposed in the form; the remaining fetch options are fixed by the spec:"
        ),
        table(
            [
                ["Parameter", "Value", "Effect"],
                ["patrol_types", "User-set (default: empty)",
                 "Patrol type value(s) to analyse. Leave empty to include all patrol types."],
                ["status", "[done]",
                 "Only completed patrols are included. Active, scheduled, or cancelled patrols are ignored."],
                ["patrols_overlap_daterange", "true",
                 "A patrol is included if any part of it overlaps the time range, not only if it starts inside it."],
                ["include_patrol_details", "true",
                 "Patrol metadata (including the patrol ID) is attached to every observation."],
                ["raise_on_empty", "true",
                 "If no patrol observations are found, the workflow stops with an error rather than producing an empty map."],
                ["sub_page_size", "200", "Page size used when paging through patrols in the EarthRanger API."],
            ],
            [4.2*cm, 3.6*cm, 8.7*cm],
        ),

        sp(4), h2("2.3 Base Map Tile Layers"),
        p(
            "The background map is configured by <code>set_base_maps_pydeck</code>. It ships "
            "with two stacked ArcGIS tile layers, both user-editable in the form. The first "
            "layer in the list is drawn at the bottom:"
        ),
        table(
            [
                ["Order", "Tile service", "Opacity", "Max zoom"],
                ["1 (bottom)", "ArcGIS World Topo Map", "1.0", "20"],
                ["2 (top)", "ArcGIS World Imagery", "0.5", "20"],
            ],
            [2.5*cm, 7*cm, 3*cm, 4*cm],
        ),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Observations → Relocations"),
        p(
            "Raw patrol observations are converted into a standardised <b>relocations "
            "GeoDataFrame</b> by <code>process_relocations</code>. Only the following "
            "columns are retained:"
        ),
        table(
            [
                ["Column", "Description"],
                ["groupby_col", "Subject (tracked device / patrol leader) identifier used to build tracks"],
                ["fixtime", "UTC datetime of the GPS fix"],
                ["junk_status", "True if the fix is flagged as junk in EarthRanger"],
                ["geometry", "Point geometry (WGS 84)"],
                ["extra__created_at", "Record creation timestamp"],
                ["patrol_id", "Identifier of the patrol the fix belongs to"],
            ],
            [4*cm, 12.5*cm],
        ),
        p("Three known-bad coordinate pairs are filtered out unconditionally:"),
        bullet("(180.0, 90.0) — boundary sentinel"),
        bullet("(0.0, 0.0) — null-island artefact"),
        bullet("(1.0, 1.0) — common default / test value"),

        sp(4), h2("3.2 Trajectory Segment Filter"),
        p(
            "A <b>trajectory segment filter</b> defines which segments between consecutive "
            "fixes are kept. It is not a separate task in this workflow: the "
            "<code>trajectory_segment_filter</code> argument of "
            "<code>relocations_to_trajectory</code> is left unset in the spec, so it appears "
            "as an advanced field under the <b>Relocations To Trajectory</b> step of the form. "
            "All six thresholds are user-configurable and default to the "
            "<code>ecoscope-platform</code> <code>TrajectorySegmentFilter</code> values:"
        ),
        table(
            [
                ["Parameter", "Default", "Unit", "Purpose"],
                ["min_length_meters", "0.001",   "m",    "Remove sub-centimetre GPS noise"],
                ["max_length_meters", "100 000", "m",    "Remove only extreme jumps (&gt; 100 km)"],
                ["min_time_secs",     "1",       "s",    "Remove zero-duration segments"],
                ["max_time_secs",     "172 800", "s",    "Remove gaps &gt; 48 h (device off / signal lost)"],
                ["min_speed_kmhr",    "0.01",    "km/h", "Remove near-stationary segments"],
                ["max_speed_kmhr",    "500",     "km/h", "Remove only physically impossible speeds"],
            ],
            [4*cm, 2.3*cm, 1.8*cm, 8.4*cm],
        ),
        note(
            "These defaults are deliberately permissive so that foot, vehicle, motorbike, and "
            "aerial patrols are all retained. The trade-off is that long straight segments "
            "spanning GPS gaps (up to 100 km or 48 h) are kept and are drawn across every cell "
            "they cross, crediting those cells with a visit. For foot patrols, tighter limits "
            "such as max 5 000 m, 21 600 s, and 9 km/h give a more faithful coverage map."
        ),

        sp(4), h2("3.3 Relocations → Trajectories"),
        p(
            "Relocations are joined into <b>linear trajectory segments</b> by "
            "<code>relocations_to_trajectory</code>. Each segment connects two consecutive "
            "fixes of the same subject; segments outside the filter limits above are then "
            "dropped. Each segment records, among other attributes:"
        ),
        bullet("<b>dist_meters</b> — straight-line distance between the two fixes"),
        bullet("<b>timespan_seconds</b> — elapsed time between the two fixes"),
        bullet("<b>speed_kmhr</b> — average speed over the segment"),
        bullet("<b>geometry</b> — LineString in WGS 84"),
        p(
            "Subjects with only a single relocation in the period cannot form a segment and "
            "are excluded (a <code>UserWarning</code> is logged for each)."
        ),

        sp(4), h2("3.4 Column Mapping"),
        p(
            "The trajectory builder carries non-core relocation columns through with an "
            "<code>extra__</code> prefix. <code>map_columns</code> renames "
            "<code>extra__patrol_id</code> back to <code>patrol_id</code>, which the "
            "coverage grid requires. No columns are dropped, and missing columns do not "
            "raise an error (<code>raise_if_not_found: false</code>)."
        ),
    ]

    # ── 4. Coverage Grid ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Patrol Coverage Grid — Methodology"), hr(),
        p(
            "The core calculation is performed by <code>create_patrol_coverage_grid</code> "
            "(package <code>ecoscope-workflows-ext-mnc</code>)."
        ),

        h2("4.1 Grid Construction"),
        p(
            "A regular square mesh is generated over the extent of the trajectories by "
            "<code>create_meshgrid</code>, using the user-set <b>Grid Cell Size</b> "
            "(default <b>1 000</b>) as the cell edge length. Only cells that intersect a "
            "trajectory are generated (<code>intersecting_only: true</code>). The grid is "
            "built in <b>EPSG:3857 (Web Mercator)</b>, and each cell receives a "
            "<code>grid_id</code>."
        ),
        note(
            "Cell size is measured in EPSG:3857 units. Web Mercator stretches distances by a "
            "factor of 1 / cos(latitude): near the equator (e.g. East Africa, within ±5°) "
            "this is under 0.4 %, so a 1 000 unit cell is effectively 1 km. At 20° from the "
            "equator, cells are about 6 % smaller on the ground than the nominal size, and "
            "about 15 % smaller at 30°."
        ),

        h2("4.2 Segment Clipping &amp; Time Allocation"),
        p(
            "Trajectory segments are reprojected to the grid CRS; segments with zero length "
            "are discarded. The remaining segments are intersected with the grid "
            "(<code>geopandas.overlay</code>, <code>how=\"intersection\"</code>), splitting "
            "each segment into the pieces that fall inside each cell. For each piece:"
        ),
        bullet("<b>clipped_dist_meters</b> = length of the piece inside the cell"),
        bullet(
            "<b>clipped_timespan_seconds</b> = segment timespan × (clipped length ÷ segment "
            "length) — time is allocated in proportion to distance, assuming constant speed "
            "along the segment"
        ),

        h2("4.3 Per-Cell Metrics"),
        p("The clipped pieces are grouped by <code>grid_id</code> and aggregated:"),
        table(
            [
                ["Column", "Calculation", "Used on map"],
                ["unique_patrol_count", "Number of distinct patrol_id values with at least one piece in the cell", "Yes — classified and coloured"],
                ["time_spent_seconds", "Sum of clipped_timespan_seconds", "No"],
                ["time_spent_hours", "time_spent_seconds ÷ 3 600, rounded to 2 dp", "No"],
                ["distance_patrolled_meters", "Sum of clipped_dist_meters", "No"],
                ["distance_patrolled_km", "distance_patrolled_meters ÷ 1 000, rounded to 2 dp", "No"],
            ],
            [4.3*cm, 8.2*cm, 4*cm],
        ),
        p("The result is sorted by <code>unique_patrol_count</code>, highest first."),

        h2("4.4 Empty Cells and Area of Interest"),
        p(
            "The spec fixes <code>keep_empty_cells: false</code>, so cells with no patrol "
            "activity are dropped and the map only shows visited cells. It also fixes "
            "<code>aoi: null</code>, so the grid follows the trajectory extent rather than a "
            "protected-area boundary. Neither option is exposed in the form; changing them "
            "requires editing <code>spec.yaml</code> and recompiling."
        ),
    ]

    # ── 5. Classification ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Classification &amp; Styling"), hr(),

        h2("5.1 Classification"),
        p(
            "<code>apply_classification</code> bins <code>unique_patrol_count</code> into "
            "<b>5 classes</b> using the <b>Equal Interval</b> scheme: the range between the "
            "least- and most-visited cells is divided into five bins of equal width. Bin "
            "labels are written as ranges with 0 decimal places (for example "
            "<code>1 - 4</code>) into the <code>patrol_count_bins</code> column."
        ),
        note(
            "Equal interval is sensitive to outliers. If one cell (e.g. a ranger post) is "
            "visited by far more patrols than anywhere else, most cells will fall into the "
            "lowest bin. In that case, consider switching the scheme in "
            "<code>spec.yaml</code> to <code>quantile</code> or <code>natural_breaks</code>."
        ),

        h2("5.2 Colour Map"),
        p(
            "<code>apply_color_map</code> assigns each bin a colour from the matplotlib "
            "<b>RdYlGn</b> (red–yellow–green) colormap and stores it in "
            "<code>bin_colors</code>."
        ),

        h2("5.3 Grid Layer Style"),
        table(
            [
                ["Property", "Value"],
                ["Fill", "bin_colors, opacity 65 %"],
                ["Outline", "Black, 0.75 px (pixel units)"],
                ["Pickable", "Yes (enables hover interaction)"],
                ["Legend", "Title “Grid visits”, labels from patrol_count_bins, bottom-right"],
            ],
            [4*cm, 12.5*cm],
        ),
    ]

    # ── 6. Map & Dashboard ────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Map &amp; Dashboard"), hr(),
        bullet(
            "<b>View state</b> — <code>compute_view_state_from_gdf</code> fits the initial "
            "camera to the extent of the classified grid (pitch 0, bearing 0, max zoom 18)."
        ),
        bullet(
            "<b>Map</b> — <code>draw_map</code> (package <code>ecoscope-workflows-ext-big-life</code>) "
            "renders the grid layer over the base map tiles as an interactive DeckGL map "
            "(max zoom 20)."
        ),
        bullet(
            "<b>Persist</b> — <code>persist_text</code> writes the map HTML to "
            "<code>patrol_grid_visits.html</code> in the results directory."
        ),
        bullet(
            "<b>Dashboard</b> — <code>create_map_widget_single_view</code> wraps the map in a "
            "widget titled <b>Patrol Grid Visits</b>, and <code>gather_dashboard</code> "
            "assembles the dashboard with the workflow details and time range."
        ),
    ]

    # ── 7. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Output Files"), hr(),
        p(
            "All outputs are written to the directory defined by the "
            "<code>ECOSCOPE_WORKFLOWS_RESULTS</code> environment variable."
        ),
        table(
            [
                ["File", "Format", "Content"],
                ["patrol_grid_visits.html", "HTML", "Interactive patrol grid visit map"],
                ["Dashboard", "Runner UI", "Single-widget dashboard containing the map"],
            ],
            [5.5*cm, 2.5*cm, 8.5*cm],
        ),
    ]

    # ── 8. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("8. Workflow Execution Logic"), hr(),

        h2("8.1 Grouping"),
        p(
            "Groupers are set to an empty list, so the workflow produces <b>one map</b> "
            "covering all selected patrols. There are no per-subject or per-period views."
        ),

        h2("8.2 Skip Conditions"),
        p("Every task inherits two default skip conditions:"),
        bullet("<b>any_is_empty_df</b> — if any input DataFrame is empty, the task is skipped rather than raising an error."),
        bullet("<b>any_dependency_skipped</b> — if an upstream task was skipped, all tasks that depend on it are skipped too."),
        note(
            "Because <code>get_patrol_observations</code> uses <code>raise_on_empty: true</code>, "
            "an empty patrol query fails the run with an error at the first data step "
            "instead of silently producing an empty dashboard."
        ),
    ]

    # ── 9. Software Versions ──────────────────────────────────────────────────
    story += [
        sp(4), h1("9. Software Versions"), hr(),
        p("The workflow's requirements, as pinned in <code>spec.yaml</code>:"),
        table(
            [
                ["Package",                            "Version",              "Role"],
                ["ecoscope-platform",                  "2.18.0",               "Core task library and workflow engine"],
                ["ecoscope-workflows-ext-mnc",         "1.0.5",                "Patrol coverage grid task"],
                ["ecoscope-workflows-ext-big-life",    "1.0.2.*",              "draw_map task"],
                ["ecoscope-workflows-ext-custom",      "0.1.0rc14.*",          "create_geojson_layer task"],
                ["ecoscope-workflows-ext-ste",         "0.0.0rc1.*",           "STE utility tasks"],
                ["ecoscope-workflows-ext-wwf-virunga", "0.0.0rc9.*",           "Shared custom tasks"],
                ["ecoscope-workflows-ext-mep",         "1.0.4",                "Shared custom tasks"],
                ["pydeck",                             "0.9.2",                "Renders the interactive DeckGL map"],
                ["opentelemetry-sdk",                  "&gt;=1.20.0, &lt;2.0.0", "Workflow run telemetry"],
            ],
            [5.5*cm, 3.5*cm, 7.5*cm],
        ),
        p(
            "<code>ecoscope-platform</code> is pulled from the <code>ecoscope-workflows</code> "
            "prefix.dev channel; the <code>ecoscope-workflows-ext-*</code> packages from the "
            "<code>ecoscope-workflows-custom</code> channel; <code>pydeck</code> and "
            "<code>opentelemetry-sdk</code> from <code>conda-forge</code>. The runtime "
            "environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ─────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
