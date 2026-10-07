# Patrol Grid Visit Workflow

Maps how often each part of a landscape is visited by ranger patrols. The workflow pulls completed patrol tracks from EarthRanger, lays a square grid over the patrolled area, and counts how many distinct patrols passed through each grid cell. The result is a colour-classified coverage map and an interactive dashboard.

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Author** | Tevin Temu, Wildlife Dynamics ([tevin@wildlifedynamics.com](mailto:tevin@wildlifedynamics.com)) |
| **Data source** | EarthRanger (completed patrols) |

## How it works

Track points from completed (done) EarthRanger patrols that overlap the analysis period are converted to trajectory segments. Segments outside configurable length, duration, and speed limits are dropped; by default only extreme outliers are removed (longer than 100 km or 48 hours, or faster than 500 km/h). A square grid (1000 m cells by default, built in Web Mercator) is laid over the trajectories and the segments are clipped to each cell. For each cell, the workflow counts the distinct patrols that entered it and totals the time spent and distance patrolled. Time is allocated in proportion to the length of each segment inside the cell. Visit counts are classified into five equal-interval bins.

## What it produces

| Output | Description |
|--------|-------------|
| **Patrol Grid Visits map** | Grid cells colored by the number of distinct patrols that entered them, classified into 5 equal-interval bins (red–yellow–green) |
| **Dashboard** | Interactive dashboard containing the map, the workflow details, and the analysis time range |

## Requirements

- Access to an **EarthRanger** instance with a configured data source
- Patrols in that instance with status **done** and recorded tracks in the analysis period

---

## 1. Load the Workflow

In the workflow runner, add a new template using this repository's URL:

```
https://github.com/wildlife-dynamics/patrol-grid-visit.git
```

Once added, select **Patrol Grid Visit** from the available templates list to load it.

---

## 2. Configure the Workflow

You'll be prompted to fill in the following parameters before running.

### Workflow Details

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional description |

### Time Range

| Field | Description | Default |
|-------|-------------|---------|
| Since | Start date/time of the analysis period | — |
| Until | End date/time of the analysis period | — |
| Timezone | Timezone used to interpret Since/Until | — |
| Time Format | Format used to display dates in the dashboard | `%d %b %Y %H:%M:%S` |

Any patrol that **overlaps** the range is included, even if it started before **Since** or ended after **Until**.

### Data Source Connection

| Field | Description |
|-------|-------------|
| Data Source | Select (or create) the EarthRanger connection to pull patrols from |

### Patrol Observations

| Field | Description | Default |
|-------|-------------|---------|
| Patrol Types | The patrol type value(s) to analyse, as configured in EarthRanger. **Leave empty to include all patrol types** | empty |

Only patrols with status **done** are fetched. If no matching patrol observations are found, the run stops with an error.

### Base Map Layers

The background tile layers shared by the map. The first layer in the list is drawn at the bottom. URL, opacity, and max zoom are editable.

| Layer | Default URL | Opacity | Max Zoom |
|-------|-------------|---------|----------|
| 1 (bottom) | ArcGIS World Topo Map | `1.0` | `20` |
| 2 (top) | ArcGIS World Imagery | `0.5` | `20` |

### Relocations To Trajectory — Segment Filter *(advanced)*

Removes GPS noise and unrealistic movements when patrol track points are joined into segments.

| Field | Default | Description |
|-------|---------|-------------|
| Min Length Meters | `0.001` | Discard segments shorter than this distance |
| Max Length Meters | `100000` | Discard segments longer than this distance (100 km) |
| Min Time Secs | `1` | Discard segments shorter than this duration |
| Max Time Secs | `172800` | Discard segments longer than this duration (48 hours) |
| Min Speed Kmhr | `0.01` | Discard segments below this average speed |
| Max Speed Kmhr | `500` | Discard segments above this average speed |

> **Note:** The defaults are permissive so that foot, vehicle, motorbike, and aerial patrols are all kept. The trade-off is that long straight lines across GPS gaps are kept too, and every cell they cross is counted as visited. For foot patrols, tighter limits (e.g. max `5000` m, `21600` s, `9` km/h) give a more faithful map.

### Patrol Coverage Grid

| Field | Default | Description |
|-------|---------|-------------|
| Grid Cell Size | `1000` | Edge length of each square grid cell, in meters. Smaller cells give a finer map but each cell gets fewer visits |

---

## 3. Run the Workflow

Once all parameters are configured, submit the workflow. The runner will:

1. Fetch the tracks of completed patrols from EarthRanger for the selected patrol types and time range.
2. Join the track points into trajectory segments, dropping segments outside the segment filter limits.
3. Build a square grid over the patrolled area and count the distinct patrols that entered each cell.
4. Classify the counts into 5 equal-interval bins and color them red–yellow–green.
5. Draw the interactive map and dashboard, and save outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

### Output Files

| File | Description |
|------|-------------|
| `patrol_grid_visits.html` | Interactive patrol grid visits map |

---

## More Help

- **Full documentation site:** [wildlife-dynamics.github.io/patrol-grid-visit](https://wildlife-dynamics.github.io/patrol-grid-visit/) — user guide, technical guide, and troubleshooting
- **Technical guide (PDF):** [`technical_guide/patrol_grid_visit_technical_guide.pdf`](technical_guide/patrol_grid_visit_technical_guide.pdf)
- **Issues:** [github.com/wildlife-dynamics/patrol-grid-visit/issues](https://github.com/wildlife-dynamics/patrol-grid-visit/issues)

## Development

This workflow's code (`ecoscope-workflows-patrol-grid-visit-workflow/`) is generated from [`spec.yaml`](spec.yaml). After editing it, recompile and commit the generated changes:

```
pixi run --manifest-path pixi.toml --locked bash -c "./dev/recompile.sh --update"
```

To regenerate the technical guide PDF after changing the workflow:

```
cd technical_guide && python3 generate_technical_guide.py
cp patrol_grid_visit_technical_guide.pdf ../docs/assets/
```

## License

[BSD 3-Clause](LICENSE)
