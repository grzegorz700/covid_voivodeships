class PageIDS:
    DAILY_STATE = 'day-state'
    DAILY_CHANGE = 'day-change'

    URL_PAGE_LOCATION = 'url-page'
    HEADER = 'chars-header'
    LAST_UPDATE = 'last-update-label'


class TabIDs:
    TAB_BAR = 'tabs'
    TAB_DIV_CONTENT = 'tabs-content'

    LINE_SPREAD = 'shape-of-spread-tab'
    DAILY_PIECHART = 'daily-cases-piechart-tab'
    VOIV_GRID = 'voiv-grid-tab'
    CASES_PER_WEEK = 'cases-per-week-tab'


class OptionsIDs:
    GRAPHS_COLUMNS_SWITCHER = 'grid-picker'
    COMMON_AXIS = 'common-yaxis-checklist'
    DATE_RANGE = 'date-range-picker'
    NO_INTEREST_ALERT = 'no-interest-chosen-alert'
    INTERESTED_DATA_PICKER = 'interested-data-checklist'
    UPDATE_SPINNER = 'update-spinner'
    CHECK_UPDATE = 'update-data-btn'
    SHOW_OPTIONS_BTN = 'options-collapse-btn'
    NORMALIZATION = 'normalization-picker'
    MOVING_AVG = 'moving-average-picker'
    OPTIONS_COLLAPSE = 'options-collapse'


class GraphIDs:
    GRAPHS_ROW = 'row-of-plots'
    MAIN_SUBGRAPHS = 'main-subgraphs'
    SHAPE_OF_SPREAD = 'graph-shape-of-spread'
    DAY_CASES_PIECHART = 'graph-daily-cases-piechart'
    DAY_CASES_PER_WEEK = 'graph-day-cases-per-week'

    @staticmethod
    def get_main_separate_voiv_map_id(voiv_name):
        return f'graph_v2-{voiv_name}'


class BadgesIDs:
    INFECTED = 'infected-badge'
    ILL = 'ill-badge'
    HEALTHY = 'healthy-badge'
    DEAD = 'dead-badge'


class IDS:
    MAP_HOVER_GRAPH = 'hover-graph'
    MAP_HOVER_HEADER = 'map-hover-txt'
    Page = PageIDS()
    Tab = TabIDs()
    Options = OptionsIDs()
    Graphs = GraphIDs()
    Badges = BadgesIDs()
    MAP = 'voivs-map'
