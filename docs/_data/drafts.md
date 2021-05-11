* **CAZymes** \
Tool [dbcan](https://github.com/linnabrown/run_dbcan)
Standalone version of dbcan.

* **MEROPS** \
A local database is created from [MEROPS](ftp://ftp.ebi.ac.uk/pub/databases/merops/current_release/merops_scan.lib).
Then a blastp against faa files is performed.




from nav.html - removed:
{}
{%- assign sections = sections | split: "|" | uniq | sort %}
{%- for section in sections %}
    <p class="caption"><span class="caption-text">{{ section }}</span></p>
    {%- for nav_item in nav %}
        {%- assign path_array = nav_item.dir | split: "/" %}
        {%- assign page_section = path_array[1] %}
        {%- if page_section == section and nav_item.hide != true and nav_item.nav_exclude != true %}
            {%- if nav_item.url == page.url %}
                {%- include toc.html html=content sanitize=true h_max=4 item_class="toctree-l%level%" %} 
                {%- if nav_item.url == page.url %}
                    {%- assign previous_page = last_loop_page %}
                    {%- assign set_next_page = true %}
                {%- endif %}
            {%- else %}
                <ul>
                    <li class="toctree-l1">
                        <a class="reference internal" href="{{ nav_item.url | absolute_url}}">{{ nav_item.title }}</a>
                    </li>
                </ul>
                {%- assign last_loop_page = nav_item %}
                {%- if set_next_page %}
                    {%- assign next_page = nav_item %}
                    {%- assign set_next_page = false %}
                {% endif %}
            {%- endif %}
        {%- endif %}
    {%- endfor %}
{%- endfor %}