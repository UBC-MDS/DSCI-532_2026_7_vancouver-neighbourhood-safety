from playwright.sync_api import Page, expect
from shiny.playwright import controller
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

app = create_app_fixture(["../src/app.py"])

# Helper function to navigate to the main dashboard tab
def go_main(page):
    page.get_by_role("tab", name="Main dashboard").click()
    page.wait_for_timeout(400)

# Helper function to navigate to the LLM Chat tab
def go_chat(page):
    page.get_by_role("tab", name="LLM Chat").click()
    page.wait_for_timeout(400)

def test_sidebar_filters(page: Page, app: ShinyAppProc):
    """
    This test verifies that filters update correctly when selections are changed
    """
    page.goto(app.url)

    go_main(page)

    nb = controller.InputSelectize(page, "nb")
    nb.set(["Downtown"])
    nb.expect_selected(["Downtown"])

    crime = controller.InputSelectize(page, "crime_type")
    crime.set(["Mischief"])
    crime.expect_selected(["Mischief"])

    month = controller.InputSelectize(page, "month")
    month.set(["January"])
    month.expect_selected(["January"])

    time = controller.InputSelectize(page, "daily_time")
    time.set(["Morning"])
    time.expect_selected(["Morning"])

def test_clear_filters_button(page: Page, app: ShinyAppProc):
    """
    This test checks that clicking the "Clear All Filters" button resets the sidebar filter inputs to an empty selection state after filters have been applied
    """
    page.goto(app.url)

    go_main(page)

    nb = controller.InputSelectize(page, "nb")
    crime = controller.InputSelectize(page, "crime_type")

    nb.set(["Downtown"])
    crime.set(["Mischief"])

    clear_btn = controller.InputActionButton(page, "clear_filters")
    clear_btn.click()

    # Shiny reactivity small wait
    page.wait_for_timeout(500)

    nb.expect_selected([])
    crime.expect_selected([])

def test_map_layer_switches(page: Page, app: ShinyAppProc):
    """
    This test verifies that map layer toggle switches (heatmap, points, and rate layers) correctly change their checked state when interacted with
    """
    page.goto(app.url)

    go_main(page)

    heat = controller.InputSwitch(page, "show_heatmap")
    heat.expect_checked(True)
    heat.set(False)
    heat.expect_checked(False)

    pts = controller.InputSwitch(page, "show_points")
    pts.expect_checked(False)
    pts.set(True)
    pts.expect_checked(True)

    rates = controller.InputSwitch(page, "show_rates")
    rates.expect_checked(False)
    rates.set(True)
    rates.expect_checked(True)

def test_download_button(page: Page, app: ShinyAppProc):
    """
    This test verifies that the "Download data" button in the LLM Chat tab correctly displays the text "Download data" and is clickable
    """
    page.goto(app.url)

    go_chat(page)

    download_btn = page.locator("#download_filtered")
    expect(download_btn).to_have_text("Download data")