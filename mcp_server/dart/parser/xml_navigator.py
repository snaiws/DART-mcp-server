from bs4 import BeautifulSoup, NavigableString
import json
import pandas as pd

class XMLNavigator:
    def __init__(self, path_xml: str):
        """BeautifulSoup으로 XML 파싱"""
        # 일반적인 시도 순서
        encodings = [
            'utf-8',        # 최우선
            'cp949',        # Windows 한글
            'euc-kr',       # 유닉스 한글
            'iso-2022-kr',  # 국제 표준
            'utf-16',       # 유니코드 16비트
            'ascii'         # 영문만
        ]

        for encoding in encodings:
            try:
                with open(path_xml, 'r', encoding=encoding) as file:
                    xml_content = file.read()
                print(f"성공: {encoding}")
                break
            except UnicodeDecodeError:
                print(f"실패: {encoding}")
                continue
            
        self.soup = BeautifulSoup(xml_content, 'xml')
    
    # 1단계: 구조 탐색
    def get_structure(self, max_depth: int = 4) -> str:
        """전체 구조 간단히 보기"""
        def build_tree(element, depth=0):
            if depth > max_depth or isinstance(element, NavigableString):
                return []
            
            lines = []
            indent = "  " * depth
            
            child_counts = {}
            for child in element.children:
                if hasattr(child, 'name') and child.name:
                    child_counts[child.name] = child_counts.get(child.name, 0) + 1
            
            for tag_name, count in child_counts.items():
                lines.append(f"{indent}- {tag_name} ({count})")
                
                if depth < max_depth:
                    for child in element.children:
                        if hasattr(child, 'name') and child.name == tag_name:
                            lines.extend(build_tree(child, depth + 1))
                            break
            
            return lines
        
        root = next((elem for elem in self.soup.children if hasattr(elem, 'name')), None)
        if not root:
            return "구조 없음"
        
        lines = [f"- {root.name} (1)"]
        lines.extend(build_tree(root, 1))
        return "\n".join(lines)
    
    # 2단계: 목차 파악 (사용자 선택)
    def get_contents(self, title_tags: list = None, section_tags: list = None) -> str:
        """문서 목차/제목 구조 (태그 선택 가능)"""
        if title_tags is None:
            title_tags = ['TITLE']
        if section_tags is None:
            section_tags = ['SECTION-1', 'SECTION-2']
        
        result = []
        
        # 제목들
        titles = []
        for tag in title_tags:
            titles.extend(self.soup.find_all(tag))
        
        if titles:
            result.append("# 제목들:")
            for i, title in enumerate(titles[:10], 1):
                text = title.get_text(strip=True)[:100]
                result.append(f"{i}. [{title.name}] {text}")
        
        # 섹션 구조
        sections = []
        for tag in section_tags:
            sections.extend(self.soup.find_all(tag))
        
        if sections:
            result.append("\n# 섹션 구조:")
            for section in sections[:10]:
                # 해당 섹션 내에서 제목 찾기
                section_title = None
                for tag in title_tags:
                    section_title = section.find(tag)
                    if section_title:
                        break
                
                title_text = section_title.get_text(strip=True)[:80] if section_title else "제목없음"
                
                # 테이블 정보 상세히
                tables = section.find_all('TABLE') + section.find_all('table')
                table_count = len(tables)
                
                table_info = f"(테이블 {table_count}개"
                if table_count > 0 and table_count <= 3:
                    # 테이블이 적으면 첫 번째 테이블의 첫 행 내용 보여주기
                    first_table = tables[0]
                    first_row = first_table.find('TR') or first_table.find('tr')
                    if first_row:
                        cells = first_row.find_all(['TD', 'TH', 'td', 'th'])
                        if cells:
                            first_row_text = " | ".join([cell.get_text(strip=True) for cell in cells[:3]])
                            table_info += f" - 예: {first_row_text[:50]}..."
                
                table_info += ")"
                
                result.append(f"- {section.name}: {title_text} {table_info}")
        
        return "\n".join(result) if result else "목차 정보 없음"
    
    # 3단계: 타겟 쿼리
    def query_simple(self, selector: str, limit: int = 5) -> str:
        """간단한 쿼리 결과"""
        try:
            if any(char in selector for char in [' ', '>', '+', '~', '[', '.', '#']):
                elements = self.soup.select(selector)
            else:
                elements = self.soup.find_all(selector)
            
            if not elements:
                return f"'{selector}' 결과 없음"
            
            results = []
            for i, elem in enumerate(elements[:limit], 1):
                if isinstance(elem, NavigableString):
                    continue
                
                text = elem.get_text(strip=True)
                preview = text[:50] + "..." if len(text) > 50 else text
                results.append(f"{i}. {elem.name}: {preview}")
            
            total = len(elements)
            showing = len(results)
            
            return f"'{selector}' 총 {total}개 (보여주는 것: {showing}개)\n" + "\n".join(results)
            
        except Exception as e:
            return f"쿼리 오류: {str(e)}"
    
    def get_table_csv(self, table_index: int) -> str:
        """테이블을 CSV 형태로 변환"""
        try:
            # 대소문자 모두 찾기
            tables = self.soup.find_all('TABLE') + self.soup.find_all('table')
            
            if table_index < 1 or table_index > len(tables):
                return f"테이블 인덱스 오류: 1-{len(tables)} 범위"
            
            table = tables[table_index - 1]
            
            # 헤더 찾기 (대소문자 모두)
            headers = []
            thead = table.find('THEAD') or table.find('thead')
            if thead:
                header_row = thead.find('TR') or thead.find('tr')
                if header_row:
                    headers = [cell.get_text(strip=True) for cell in header_row.find_all(['TH', 'TD', 'th', 'td'])]
            
            # 데이터 행들 (대소문자 모두)
            tbody = table.find('TBODY') or table.find('tbody')
            if tbody:
                rows = tbody.find_all('TR') + tbody.find_all('tr')
            else:
                rows = table.find_all('TR') + table.find_all('tr')
                if headers:  # 헤더가 있으면 첫 번째 행 제외
                    rows = rows[1:]
            
            # CSV 생성
            csv_lines = []
            data = []
            
            for row in rows:
                cells = [cell.get_text(strip=True) for cell in row.find_all(['TD', 'TH', 'td', 'th'])]
                if cells:  # 빈 행이 아니면
                    data.append(cells)
            
            if not data:
                return f"테이블 {table_index}: 데이터 없음"
            
            # 컬럼 수 맞추기
            max_cols = max(len(row) for row in data) if data else 0
            for row in data:
                while len(row) < max_cols:
                    row.append("")
            
            # CSV 문자열 생성
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # 헤더 추가
            if headers and len(headers) == max_cols:
                writer.writerow(headers)
            else:
                writer.writerow([f"Col{i+1}" for i in range(max_cols)])
            
            # 데이터 추가
            for row in data:
                writer.writerow(row)
            
            csv_content = output.getvalue()
            output.close()
            
            return csv_content
            
        except Exception as e:
            return f"CSV 변환 오류: {str(e)}"


# 3단계 함수들
async def xmlparser_step1_structure(path_xml: str, max_depth: int = 4) -> str:
    """1단계: 구조 탐색"""
    navigator = XMLNavigator(path_xml)
    return [navigator.get_structure(max_depth)]

async def xmlparser_step2_contents(path_xml: str, title_tags: list = None, section_tags: list = None) -> str:
    """2단계: 목차 파악 (태그 선택 가능)"""
    navigator = XMLNavigator(path_xml)
    return [navigator.get_contents(title_tags, section_tags)]

async def xmlparser_step3_query(path_xml: str, selector: str, limit: int = 5) -> str:
    """3단계(1): 타겟 쿼리"""
    navigator = XMLNavigator(path_xml)
    return [navigator.query_simple(selector, limit)]

async def xmlparser_get_table_csv(path_xml: str, table_index: int) -> str:
    """3단계(2): 테이블을 CSV로 변환"""
    navigator = XMLNavigator(path_xml)
    return [navigator.get_table_csv(table_index)]