import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from models.product import Product

st.set_page_config(
    page_title="Product Crawler",
)

# Initialize session state for visualization toggle
if "show_visualizations" not in st.session_state:
    st.session_state.show_visualizations = False


# Placeholder function to simulate data retrieval from different crawlers
def get_crawled_data(link, crawler_type, max_items):
    # Placeholder data for demonstration purposes
    if crawler_type == "Amazon CA":
        products = []
    elif crawler_type == "Source Office Furniture":
        products = []
    elif crawler_type == "Toysrus CA":
        products = []
    elif crawler_type == "Uline":
        products = []
    elif crawler_type == "Walmart CA":
        products = []
    elif crawler_type == "Staples CA":
        from websites.non_proxy import collect_data as collect_staplesca

        products = collect_staplesca(page_url=link, max_items=max_items)
    else:
        products = []

    # # Placeholder products list
    # products = [
    #     Product(
    #         name="Sample Product 1",
    #         brand="Brand A",
    #         product_number="12345",
    #         color="Red",
    #         image_url="http://example.com/image1.jpg",
    #         depth="10",
    #         height="20",
    #         width="30",
    #         weight="5",
    #         min_height="10",
    #         max_height="15",
    #         total_product_weight="5",
    #         total_boxed_weight="6",
    #         product_url="http://example.com/product1",
    #         rating_point="4.5",
    #         rating_count="100",
    #         others="None",
    #     ),
    #     Product(
    #         name="Sample Product 2",
    #         brand="Brand B",
    #         product_number="67890",
    #         color="Blue",
    #         image_url="http://example.com/image2.jpg",
    #         depth="15",
    #         height="25",
    #         width="35",
    #         weight="6",
    #         min_height="12",
    #         max_height="18",
    #         total_product_weight="6",
    #         total_boxed_weight="7",
    #         product_url="http://example.com/product2",
    #         rating_point="4.0",
    #         rating_count="150",
    #         others="None",
    #     ),
    # ]

    return products


def get_website_crawler_options() -> list[str]:
    """
    Retrieves the options available for configuring a website crawler.

    This function returns a list of strings, where each string represents an option that can be
    set for the
    website crawler.

    :return: A list of strings representing the website crawler options.
    :rtype: list of str
    """

    # return ["Staples CA", "Amazon CA", "Source Office Furniture", "Toysrus CA", "Uline", "Walmart CA"]
    return ["Staples CA"]


# Function to convert DataFrame to CSV
def to_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")


def show_visualizations(data):
    """Function to display visualizations"""
    st.header("Visualizations")

    if "total_product_weight" in data.columns:
        # Convert numerical columns to appropriate data types
        data["total_product_weight"] = pd.to_numeric(
            data["total_product_weight"], errors="coerce"
        )

    if "total_boxed_weight" in data.columns:
        data["total_boxed_weight"] = pd.to_numeric(
            data["total_boxed_weight"], errors="coerce"
        )
    if "rating_point" in data.columns:
        data["rating_point"] = pd.to_numeric(data["rating_point"], errors="coerce")
    if "rating_count" in data.columns:
        data["rating_count"] = pd.to_numeric(data["rating_count"], errors="coerce")

    # Brand Distribution
    brand_distribution = data["brand"].value_counts().reset_index()
    brand_distribution.columns = ["Brand", "Count"]
    fig_brand = px.bar(
        brand_distribution, x="Brand", y="Count", title="Brand Distribution"
    )
    st.plotly_chart(fig_brand)

    # Product Color Popularity
    color_popularity = data["color"].value_counts().reset_index()
    color_popularity.columns = ["Color", "Count"]
    fig_color = px.pie(
        color_popularity,
        names="Color",
        values="Count",
        title="Product Color Popularity",
    )
    st.plotly_chart(fig_color)

    # Plotly Bar Chart for Ratings
    if "rating_count" in data.columns and not data["rating_point"].isnull().all():
        fig1 = px.bar(
            data.dropna(subset=["rating_point"]),
            x="name",
            y="rating_point",
            color="brand",
            title="Product Ratings by Brand",
        )
        st.plotly_chart(fig1)
    else:
        st.warning("No valid data for Product Ratings by Brand chart")

    # Seaborn Distribution Plot for Product Weights
    if not data["total_product_weight"].isnull().all():
        fig2, ax2 = plt.subplots()
        sns.histplot(data["total_product_weight"].dropna(), kde=True, ax=ax2)
        ax2.set_title("Distribution of Total Product Weight")
        st.pyplot(fig2)
    else:
        st.warning("No valid data for Distribution of Total Product Weight chart")

    # Plotly Box Plot for Product Dimensions
    if not data[["depth", "height", "width"]].isnull().all().all():
        fig3 = px.box(
            data.dropna(subset=["depth", "height", "width"]),
            y=["depth", "height", "width"],
            title="Box Plot of Product Dimensions",
        )
        st.plotly_chart(fig3)
    else:
        st.warning("No valid data for Box Plot of Product Dimensions chart")

    # Plotly Scatter Plot for Rating Points vs Rating Count
    if ("rating_count" in data.columns and "rating_point" in data.columns) and not data[
        ["rating_count", "rating_point"]
    ].isnull().all().all():
        fig4 = px.scatter(
            data.dropna(subset=["rating_count", "rating_point"]),
            x="rating_count",
            y="rating_point",
            size="rating_point",
            color="brand",
            title="Rating Points vs Rating Count",
        )
        st.plotly_chart(fig4)
    else:
        st.warning("No valid data for Rating Points vs Rating Count chart")

    # Weight Analysis
    if (
        "total_product_weight" in data.columns and "total_boxed_weight" in data.columns
    ) and not data[["total_product_weight", "total_boxed_weight"]].isnull().all().all():
        fig_weight = px.scatter(
            data.dropna(subset=["total_product_weight", "total_boxed_weight"]),
            x="total_product_weight",
            y="total_boxed_weight",
            title="Total Product Weight vs. Total Boxed Weight",
        )
        st.plotly_chart(fig_weight)
    else:
        st.warning(
            "No valid data for Total Product Weight vs. Total Boxed Weight chart"
        )

    # Height Comparison
    if ("min_height" in data.columns and "max_height" in data.columns) and not data[
        ["min_height", "max_height"]
    ].isnull().all().all():
        fig_height, ax_height = plt.subplots()
        ax_height.hist(
            [data["min_height"].dropna(), data["max_height"].dropna()],
            bins=10,
            label=["Min Height", "Max Height"],
        )
        ax_height.set_title("Height Comparison")
        ax_height.set_xlabel("Height")
        ax_height.set_ylabel("Frequency")
        ax_height.legend(loc="upper right")
        st.pyplot(fig_height)
    else:
        st.warning("No valid data for Height Comparison chart")


def list_csv_files(folder_path):
    """List all CSV files in the specified folder."""
    list_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    return sorted(list_files, key=lambda x: (x != "staplesca.csv", x))


def process_csv_data(data):
    # Mapping the CSV columns to Product model fields
    data = data.rename(
        columns={
            "Name": "name",
            "Brand": "brand",
            "Product number": "product_number",
            "Color": "color",
            "Image URL": "image_url",
            "Depth": "depth",
            "Height": "height",
            "Width": "width",
            "Min height": "min_height",
            "Max height": "max_height",
            "Total product weight": "total_product_weight",
            "Total boxed weight": "total_boxed_weight",
            "Product URL": "product_url",
            "Rating": "rating_point",
            "Rating count": "rating_count",
        }
    )

    # Fill missing columns with default values
    # for column in Product.__fields__:
    #     if column not in data.columns:
    #         data[column] = ""

    return data


def main():
    st.session_state.is_disable = False
    st.title("Product Data Viewer")

    # Sidebar for user input
    st.sidebar.header("Input Options")

    input_option = st.sidebar.selectbox(
        "Choose input method", ("Upload from CSV file", "Load from Crawled Folder", "Crawl from Link"), )

    st.markdown(
        f"""
        ### Overview
        A web crawling module to extract product information from websites and view it via Streamlit.

        ### Explaination
        - Libraries: playwright, pandas
        - Proxy: use ScrapeOps to bypass proxy for some websites
        - Step:
            + Launch a new Chromium browsing context
            + Finds all product elements on the page using Playwright's query selector
            + Iterates over each product element to redirect to its URL and initiates a loop to retry fetching product details in case of failures
            + Store crawled data into csv file

        ### Input Options
        - Load from Crawled Folder (default)
        - Crawl from Link (input correct link to crawl)
    """
    )

    if input_option == "Crawl from Link":
        with st.sidebar.form("crawl_form"):
            crawl_link = st.text_input("Enter the link to crawl")
            crawler_type = st.selectbox(
                "Select the type of crawler",
                get_website_crawler_options(),
            )
            max_items = st.selectbox("Select max items", [10, 20, 30, 40])
            crawl_submit_button = st.form_submit_button(
                label="Crawl Data", disabled=st.session_state.is_disable
            )

        if crawl_submit_button and crawl_link:
            # Fetch the crawled data
            with st.spinner("Crawling..."):
                st.session_state.is_disable = True
                crawled_products = get_crawled_data(crawl_link, crawler_type, max_items)
                st.success("Crawled successfully!")

            if crawled_products:
                crawled_data = pd.DataFrame(
                    [product.dict() for product in crawled_products]
                )

                # Display the data
                st.header("Raw Product Data Table")
                st.success(
                    f"Successfully crawled and added {len(crawled_products)} products!"
                )

                st.dataframe(crawled_data, use_container_width=True)

                # Download button
                data_csv = to_csv(crawled_data)
                st.download_button(
                    label="Download as CSV",
                    data=data_csv,
                    file_name="crawled_data.csv",
                    mime="text/csv",
                )

                # Toggle button and visualization display
                if st.button("Toggle Visualizations"):
                    st.session_state.show_visualizations = (
                        not st.session_state.show_visualizations
                    )

                if st.session_state.show_visualizations:
                    show_visualizations(crawled_data)

            else:
                st.error("No data retrieved. Please check the link or crawler type.")

            st.session_state.is_disable = False

        else:
            st.info("Enter a link and select a crawler type, then click Submit.")

    elif input_option == "Upload CSV File":
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)

            processed_data = process_csv_data(data)

            # Display the data
            st.header("Raw Product Data Table")
            st.success("CSV file successfully loaded!")
            st.dataframe(processed_data, use_container_width=True)

            # Toggle button and visualization display
            if st.button("Toggle Visualizations"):
                st.session_state.show_visualizations = (
                    not st.session_state.show_visualizations
                )

            if st.session_state.show_visualizations:
                show_visualizations(processed_data)

    elif input_option == "Load from Crawled Folder":
        # List CSV files in the output folder
        output_folder = "output"
        csv_files = list_csv_files(output_folder)

        if csv_files:
            selected_file = st.sidebar.selectbox("Select a CSV file", csv_files)
            if selected_file:
                file_path = os.path.join(output_folder, selected_file)
                data = pd.read_csv(file_path)

                processed_data = process_csv_data(data)

                # Display the data
                st.header("Raw Product Data Table")
                st.success(f"Successfully loaded {selected_file}")
                st.dataframe(processed_data, use_container_width=True)

                # Toggle button for visualizations
                if st.button("Toggle Visualizations"):
                    st.session_state.show_visualizations = (
                        not st.session_state.show_visualizations
                    )

                # Show visualizations based on the toggle state
                if st.session_state.show_visualizations:
                    show_visualizations(processed_data)
        else:
            st.error("No CSV files found in the output folder.")


if __name__ == "__main__":
    main()
