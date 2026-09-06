import React, { useState, useId } from "react";
import { Layout, theme, Button, Table, ConfigProvider, Flex, Spin } from "antd";
import axios from "axios";
import { useQuery, useMutation } from "@tanstack/react-query";

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const id = useId();
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  });

  const [checkout, setCheckout] = useState(true);

  const { data, isLoading } = useQuery({
    queryKey: ["list", id, pagination.current, pagination.pageSize],
    queryFn: async () => {
      const res = await axios.get("http://127.0.0.1:8000/api/", {
        params: {
          page: pagination.current,
          page_size: pagination.pageSize,
        },
      });
      return res.data;
    },
  });

  const mutation = useMutation({
    mutationFn: async (newCar: any) => {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/prediction/",
        newCar,
      );
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
        <Sider trigger={null} width={500} collapsible collapsed={checkout}>
          {!checkout && (
            <Flex justify="center" align="center" className="!h-full">
              {mutation.isPending ? (
                <Spin />
              ) : (
                <div>
                  <span className="text-lg font-bold text-white">Result</span>
                </div>
              )}
              <Button onClick={() => setCheckout(true)}>Back</Button>
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
            <Table
              loading={isLoading}
              dataSource={data?.results || []}
              columns={[
                {
                  title: "Manufacturer",
                  dataIndex: "manufacturer",
                  key: "manufacturer",
                },
                {
                  title: "Model",
                  dataIndex: "model",
                  key: "model",
                },
                {
                  title: "Production Year",
                  dataIndex: "prod_year",
                  key: "prod_year",
                },
                {
                  title: "Fuel Type",
                  dataIndex: "fuel_type",
                  key: "fuel_type",
                },
                {
                  title: "Engine Volume",
                  dataIndex: "engine_volume",
                  key: "engine_volume",
                },
                {
                  title: "Mileage (km)",
                  dataIndex: "mileage",
                  key: "mileage",
                },
                {
                  title: "",
                  dataIndex: "id",
                  key: "id",
                  render: (id) => (
                    <Button
                      type="primary"
                      onClick={() => {
                        setCheckout(false);
                        mutation.mutate({ id });
                      }}
                    >
                      Action
                    </Button>
                  ),
                },
              ]}
              bordered
              rowKey={"id"}
              pagination={{
                current: pagination.current,
                pageSize: pagination.pageSize,
                total: data?.count || 0,
                showSizeChanger: true,
                onChange: (page, pageSize) => {
                  setPagination({ current: page, pageSize });
                },
              }}
            />
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
};

export default App;
