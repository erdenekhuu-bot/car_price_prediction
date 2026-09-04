import React, { useState, useId } from "react";
import { Layout, theme, Button, Table, ConfigProvider, Flex } from "antd";
import axios from "axios";
import { useQuery } from "@tanstack/react-query";

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
  const [collapsed, setCollapsed] = useState(true);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const id = useId();

  const { data, isLoading } = useQuery({
    queryKey: ["list", id],
    queryFn: async () => {
      const res = await axios.get("http://127.0.0.1:8000/api/");
      return res.data;
    },
  });

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#00b96b",
          colorBgContainer,
          borderRadiusLG,
        },
      }}
    >
      <Layout className="!h-screen !flex !flex-row-reverse">
        <Sider trigger={null} width={500} collapsible collapsed={collapsed}>
          {!collapsed && (
            <Flex justify="center" align="center" className="!h-full">
              <span className="text-lg font-bold text-white">Result</span>
            </Flex>
          )}
        </Sider>

        <Layout>
          <Header style={{ padding: 0, background: colorBgContainer }} />

          <Content
            style={{
              margin: "24px 16px",
              padding: 24,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Button onClick={() => setCollapsed(!collapsed)}>click</Button>
            <Table
              loading={isLoading}
              dataSource={data?.results || []}
              columns={[
                {
                  title: "ID",
                  dataIndex: "id",
                  key: "id",
                },
                {
                  title: "price",
                  dataIndex: "price",
                  key: "price",
                },
              ]}
              bordered
              rowKey={"id"}
            />
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
};

export default App;
